/*****************************************************************************
 **
 ** ocean_eval
 **
 ** Houdini Ocean Toolkit  DSO - written by  Drew.Whitehouse@anu.edu.au
 **
 ****************************************************************************/
 plugin "ocean_eval";
 
displacement ocean_eval(
							  float Km = 0.03;
							  float freq= 1;
							  float approx_height = 1;
							  float grid_res = 8;
							  float timer = 0;
							  float ocean_size = 100;
							  float height_scale =3;
							  float wind_speed = 30;
							  float smallest_wave = 0.02;
							  float wind_dir = 0;
							  float damp_refl = 0.5;
							  float wind_align = 2;
							  float ocean_depth = 200;
							  float seed = 0;
							  float do_normal = 1;
							  float do_chop = 1;
							  float chop_amount = 1;
							  float eigenvalues = 0;
							  float foamscale = 1;
							  string space = "object";
							  string convspace = "current";
							  output varying vector disp=1;
							  output varying normal nml=1;
							  output varying float jminus=1;
							  output varying float jplus=1;
							  output varying vector eminus=1;
							  output varying vector eplus=1;)
{
  /* Local variables */
  float noi;  
  float ss = P[0];
  float tt = P[2];
  point sum = 0;
  normal Nf = normalize(ntransform(space, N));
  
  point PP = transform(space, P);

  /* ocean waves */
  ocean_eval(ss, tt, timer, height_scale,
             do_chop, chop_amount, disp,
			 do_normal, nml,
			 eigenvalues, jminus, jplus, eminus, eplus,
			 grid_res, ocean_size, wind_speed, smallest_wave,
			 wind_dir, damp_refl, wind_align, ocean_depth, seed);
			
sum = PP + disp;
sum = transform(convspace, sum);
nml = ntransform(convspace, nml);

  P = P-nml *(Km*sum);
  //N = calculatenormal(P + normalize(nml) * Km);
  N = calculatenormal(P);
}
