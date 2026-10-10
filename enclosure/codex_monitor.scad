// Codex monitor display â€” dimensions in mm. Prototype, verify physical fit.
// Board: Waveshare ESP32-C6-LCD-1.47, non-touch, WITHOUT soldered headers.
part = "assembly"; // assembly, case, saddle, rear_stop, layout
$fn = 48;
board_l=36.37; board_w=20.32;
clearance=0.55; wall=2.0; case_depth=11.8;
monitor_thickness=18; pad=1; rear_gap=monitor_thickness+2*pad;
front_lip=3; // must land on structural bezel only; set 0 for adhesive-only top support
m2_clear=2.35; m3_clear=3.4;
case_l=board_l+2*(clearance+wall);
case_w=board_w+2*(clearance+wall);
// Verified asymmetric M2 threaded mount locations from manufacturer's drawing.
mounts=[[-board_l/2+2,-6.64],[-board_l/2+2,6.64],[board_l/2-2.4,-8.16],[board_l/2-2.4,8.16]];
module rounded_box(l,w,h,r=2){linear_extrude(h) offset(r=r) square([l-2*r,w-2*r],center=true);}
module bore(d,h){cylinder(d=d,h=h);}
module case(){
 difference(){
  union(){
   // Open front; the factory LCD/acrylic stays assembled. No pressure on glass.
   difference(){rounded_box(case_l,case_w,case_depth);translate([0,0,-1])rounded_box(board_l+2*clearance,board_w+2*clearance,case_depth+2,1);}
   // Rear corner bridges. Only factory threaded posts support the board.
   for(p=mounts) translate([p[0],p[1],0]) cylinder(d=6.7,h=3);
   for(p=mounts) translate([p[0],sign(p[1])*(case_w/2-2),1.5]) cube([6.7,4,3],center=true);
   for(s=[-1,1]) translate([s*23,-9,0]) rounded_box(10,9,3,2);
  }
  for(p=mounts) translate([p[0],p[1],-1])bore(m2_clear,5);
  for(s=[-1,1]) translate([s*23,-9,-1])bore(m3_clear,5);
  // Full-width end opening clears USB plug; measure user's molded plug first.
  translate([board_l/2-1,-7,3])cube([10,14,case_depth]);
  // Both side buttons accessible without printed actuators.
  for(s=[-1,1])translate([8,s*(case_w/2)-4,3])cube([10,8,case_depth]);
 }
}
module slot(len,d,h){hull(){translate([0,0,0])bore(d,h);translate([0,len,0])bore(d,h);}}
module saddle(){
 difference(){
  union(){
   translate([0,22,0])rounded_box(36,48,3,2);
   // Tiny forward locating lip: this is a gravity saddle, never a clamp.
   if(front_lip>0) translate([-18,-2,-front_lip])cube([36,2,front_lip+3]);
   translate([-4,0,0])cube([8,3,18]);
   translate([-28,0,14])cube([56,3,8]);
  }
  // Stops cover 14â€“32 mm monitor bodies with 1 mm pads each side.
  for(x=[-10,10])translate([x,21,-1])slot(18,m3_clear,5);
  for(x=[-23,23])translate([x,-1,19])rotate([-90,0,0])bore(m3_clear,6);
 }
}
module rear_stop(){
 difference(){
  union(){translate([-18,0,0])cube([36,9,3]);translate([-18,0,-18])cube([36,3,21]);}
  for(x=[-10,10])translate([x,5,-1])bore(m3_clear,6);
 }
}
module assembly(){
 color("#243348")translate([0,0,28])rotate([90,0,0])case();
 color("#455775")saddle();
 color("#647896")translate([0,rear_gap,3])rear_stop();
 // Context geometry only. Transparent gray monitor and green pads are NOT printed.
 %translate([-50,1,-50])cube([100,monitor_thickness,49]);
 %color("#4dcc98")translate([-16,1,-1])cube([32,monitor_thickness,1]);
 // LCD illustration, not a manufacturer model.
 %color("#1cdbc0")translate([-16.175,-11.9,19.3])cube([32.35,0.4,17.39]);
}
if(part=="case")case();
if(part=="saddle")translate([0,0,2])rotate([90,0,0])saddle(); // front lip on bed; brim/support the elevated mast
if(part=="rear_stop")translate([0,3,0])rotate([90,0,0])rear_stop(); // outside wall on bed
if(part=="assembly")assembly();
if(part=="layout") {case();translate([0,55,0])rotate([90,0,0])saddle();translate([0,100,0])rotate([90,0,0])rear_stop();}
