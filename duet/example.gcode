; uses Globals by DSF - here Pressure_3 is the global that we use for the Marco pressure controller, i commented out the actual moves for now

M42 P9 S1; spray off
set global.Pressure_3 =0
G4 S2
;;G1 X0 Y00 F2000


set global.Pressure_3 =1000
G4 S3
M42 P9 S0 ; spray on 
;G1 X0 Y100 F2000
M42 P9 S1 ; spray off

set global.Pressure_3 =300
G4 S3
M42 P9 S0 ; spray on 
;G1 X0 Y100 F2000
M42 P9 S1 ; spray off

set global.Pressure_3 =2000
G4 S3
M42 P9 S0 ; spray on 
;G1 X220 Y100 F2000
M42 P9 S1 ; spray off

set global.Pressure_3 =600
G4 S3
M42 P9 S0 ; spray on 
;G1 X20 Y10 F2000
M42 P9 S1 ; spray off

M42 P9 S1; spray off
set global.Pressure_3 =4000
G4 S3
;G1 X0 Y0 F2000

M42 P9 S1; spray off
set global.Pressure_3 =0
G4 S3
;G1 X0 Y0 F2000
