//    Yo emacs, this is -*- c++ -*- code.
//
//    RSL_Ocean.cpp - RSL plugin shadeop for building Ocean waves (see
//    Ocean.h for more details).
//
//     December 2008.
//     virtualritz@gmail.com
//
//

//
//     Houdini Ocean Toolkit
//     Copyright (C) 2005  Drew Whitehouse, ANU Supercomputer Facility
//     RSL Ocean shadop
//     Parts Copyright (C) 2008  Moritz Moeller
//     This RSL shadeop is a port of the VEX shadeop

//     This program is free software; you can redistribute it and/or modify
//     it under the terms of the GNU General Public License as published by
//     the Free Software Foundation; either version 2 of the License, or
//     (at your option) any later version.

//     This program is distributed in the hope that it will be useful,
//     but WITHOUT ANY WARRANTY; without even the implied warranty of
//     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//     GNU General Public License for more details.

//     You should have received a copy of the GNU General Public License
//     along with this program; if not, write to the Free Software
//     Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#include "Ocean.h"

#include <RslPlugin.h>
#include <RixInterfaces.h>

#define DELIGHT // uncomment for compiling with PRMan

//
// RSL shadeop implementing Tessendorf's ocean model
//
struct OceanHolder
{
    drw::Ocean        *ocean;
    drw::OceanContext *context;
    float              normalize_factor;

    OceanHolder() : ocean(0),context(0)
    {
        // nothing
    }

    ~OceanHolder()
    {
        if (ocean) delete ocean;
        if (context) delete context;
    }
};


static OceanHolder* oh;
RixMutex* oceanMutex = NULL;



static drw::Ocean*
ocean_from_argv(
    const RslArg* argv[] )
{

    // consumes "IFFFFFFFI" ...
    int   res  = 1 << int(*(RslFloatIter(argv[0]))); // I
    float size = *(RslFloatIter(argv[1]));    // F
    float V    = *(RslFloatIter(argv[2]));    // F
    float l    = *(RslFloatIter(argv[3]));    // F
    float w    = *(RslFloatIter(argv[4]));    // F
    float damp = *(RslFloatIter(argv[5]));    // F
    float align= *(RslFloatIter(argv[6]));    // F
    float depth= *(RslFloatIter(argv[7]));    // F
    int   seed = int(*(RslFloatIter(argv[8])));      // I

    return new drw::Ocean(res,res,size/float(res),size/float(res),
                          V,l,0.000001,w,
                          1-damp,align,depth,seed);


}


extern "C" {

void ocean_init( RixContext *ctx )
{
    RixThreadUtils *lockFactory =
       ( RixThreadUtils* ) ctx->GetRixInterface( k_RixThreadUtils );

    oceanMutex = lockFactory->NewMutex();
    oh = new OceanHolder;
}


void ocean_cleanup( RixContext *ctx )
{
    delete oh;
    if( oceanMutex ) delete oceanMutex;
}


int
    ocean_eval(
        RslContext* rslContext,
        int argc,
        const RslArg* argv[])
{
    RslFloatIter x             = argv[1]; // F
    RslFloatIter z             = argv[2]; // F
    float now                 = *(RslFloatIter(argv[3])); // F
    float height_scale         = *(RslFloatIter(argv[4])); // F

    bool do_chop               = bool(*(RslFloatIter(argv[5]))); // I
    float chop_amount          = *(RslFloatIter(argv[6])); // F
    RslVectorIter displacement  = argv[7]; // &V

    bool do_normal             = bool(*(RslFloatIter(argv[8]))); // I
    RslNormalIter normal       = argv[9]; // &V

    bool do_jacobian           = bool(*(RslFloatIter(argv[10])));    // I
    RslFloatIter  Jminus       = argv[11]; // &F
    RslFloatIter  Jplus        = argv[12]; // &F
    RslVectorIter Eminus       = argv[13]; // &V
    RslVectorIter Eplus        = argv[14]; // &V

    oceanMutex->Lock();
    int numVals = RslArg::NumValues(argc, argv);
    for (int i = 0; i < numVals; ++i ) {

        if (!oh->ocean)
        {
            oh->ocean = ocean_from_argv(argv+15);
            oh->normalize_factor = oh->ocean->get_height_normalize_factor();
            oh->context = oh->ocean->new_context(true,do_chop,do_normal,do_jacobian);
            oh->ocean->update (now,*oh->context,true,do_chop,do_normal,do_jacobian,
                               height_scale * oh->normalize_factor,chop_amount);
        }

        // We always choose the catmull rom version here, the linear
        // option is primarily for the SOP where realtime feedback is more
        // important.
        oh->context->eval2_xz(*x,*z);
        ++x;
        ++z;

        (*displacement)[0] = oh->context->disp[0];
        (*displacement)[1] = oh->context->disp[1];
        (*displacement)[2] = oh->context->disp[2];
        ++displacement;

        if (do_normal)
        {
            (*normal)[0] = oh->context->normal[0];
            (*normal)[1] = oh->context->normal[1];
            (*normal)[2] = oh->context->normal[2];
            ++normal;
        }

        if (do_jacobian)
        {
            *Jminus  = oh->context->Jminus;
            *Jplus   = oh->context->Jplus;

            (*Eminus)[0] = oh->context->Eminus[0];
            (*Eminus)[1] = oh->context->Eminus[1];
            (*Eminus)[2] = oh->context->Eminus[2];

            (*Eplus)[0] = oh->context->Eplus[0];
            (*Eplus)[1] = oh->context->Eplus[1];
            (*Eplus)[2] = oh->context->Eplus[2];

            ++Jminus;
            ++Jplus;
            ++Eminus;
            ++Eplus;
        }
    }
    oceanMutex->Unlock();

    return 0;
}


#ifdef DELIGHT
// 3Delight doesn't understand new-school signature strings yet
static RslFunction oceanFunctions[] =
{
    { "void ocean_eval("
        "float,float," // x, z,
        "float," // time,
        "float," // height_scale
        "float,float,vector," // do_chop, chop_amount, displacement
        "float,normal," // do_normal, normal
        "float,float,float,vector,vector," // do_jacobian, jm, jp, em, ep
        "float," // gridres
        "float," // ocean_size
        "float," // windspeed
        "float," // smallest_wave
        "float," // winddirection
        "float," // damp
        "float," // align
        "float," // ocean_depth
        "float)", // seed
        ocean_eval,
        ocean_init,
        ocean_cleanup },
    NULL
};
#else
static RslFunction oceanFunctions[] =
{
    { "void ocean_eval("
        "varying float,varying float," // x, z,
        "uniform float," // time,
        "uniform float," // height_scale
        "uniform float,uniform float,output varying vector," // do_chop, chop_amount, displacement
        "uniform float,output varying normal," // do_normal, normal
        "uniform float,output varying float,output varying float,output varying vector,output varying vector," // do_jacobian, jm, jp, em, ep
        "uniform float," // gridres
        "uniform float," // ocean_size
        "uniform float," // windspeed
        "uniform float," // smallest_wave
        "uniform float," // winddirection
        "uniform float," // damp
        "uniform float," // align
        "uniform float," // ocean_depth
        "uniform float)", // seed
        ocean_eval,
        ocean_init,
        ocean_cleanup },
    NULL
};
#endif

RSLEXPORT RslFunctionTable RslPublicFunctions = oceanFunctions;

} // extern "C"
