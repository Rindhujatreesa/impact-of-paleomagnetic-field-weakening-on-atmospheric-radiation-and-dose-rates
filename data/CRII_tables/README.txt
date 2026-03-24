Pre-calculated tables of cosmic ray induced ionization (CRII) in units of [ion
pairs /g /sec] – see full description in (Usoskin and Kovaltsov, Cosmic ray
induced ionization in the atmosphere: Full modeling and practical applications,
J. Geophys. Res., 111, D21206, 2006 – accessible at
http://cc.oulu.fi/~usoskin/personal/2006JD007150.pdf )
and Usoskin, Kovaltsov, Mironova, Cosmic ray induced ionization model CRAC:CRII:
An extension to the upper atmosphere, J. Geophys. Res., 115, D10302, 2010 -
accessible at http://cc.oulu.fi/~usoskin/personal/2009JD013142.pdf.
*** Please cite both the above papers when using the data *****

The tables are given in ASCII files with names S_XXXXXX.RES, where XXXXXX stands
for the residual atmospheric depth in 0.01[g/cm2], so that S_000100.RES corresponds
to the atmospheric depth of 1 g/cm2.

Each file is organized as follows:

* First line: values of the modulation potential Phi (see comment below) in MV from 0 to 1500 MV
* Following lines give: the geomagnetic cutoff rigidity Pc in GV (first number) followed by CRII
for the corresponding values of Pc (raw) and Phi (column).

In order to calculate CRII for given values of the atmospheric depth h, geomagnetic cutoff rigidity Pc
 and the modulation potential Phi, one needs to proceed as follows.
(1) open the appropriate file with the name S_XXXXXX.RES;
(2) read the value of CRII from the crossing of the appropriate raw (the value of Pc) and column (the value of Phi).
(3) If the given values of h, Pc and Phi do not coincide with the grid of the tabulated CRII, an
 interpolation can be used, since the CRII is quite a smooth function of the parameters.
We recommend power-law interpolation but a linear one also can be applied.

The user is expected to independently provide the values of Pc and Phi.

All request, concerns and comments regarding the CRII model should be addressed to Ilya Usoskin <ilya.usoskin@oulu.fi>

****** Note on the use of Phi *****

Since the exact value of the modulation potential Phi is model dependent, it is required that
the value of Phi should be calculated in the model described in (Usoskin, I.G., K. Alanko-Huotari,
G.A. Kovaltsov, K. Mursula, Heliospheric modulation of cosmic rays: Monthly reconstruction for 1951-2004,
J. Geophys. Res., 110(A12), A12108, 2005).
A table of the monthly Phi values since 1951 is given in the attached file “Phi_mon_tab.txt” or can
 be downloaded from http://cosmicrays.oulu.fi/phi/ .
In a case of the Phi values calculated in another model, they should be reduced to the requested one
using a scaling described in the Appendix to the paper (Usoskin and Kovaltsov, JGR, 110(A12), A12108,
2005 – accessible as  http://cosmicrays.oulu.fi/phi/2005JA011250.pdf), otherwise a systematic error
may occur in the computed CRII result.
