$(document).ready(function(){
   var gklimit = 2;
   var deflimit = 5;
   var midlimit = 5;
   var fwdlimit = 3;
   $("input[type='checkbox']").on('change', 
   function(evt) {      
      if($("input[name='GKP']:checked").length > gklimit) {
         this.checked = false;         
         alert("You can choose maximum 2 goalkeepers");
      }
      if($("input[name='DEF']:checked").length > deflimit) {
         this.checked = false;         
         alert("You can choose maximum 5 defenders");
      }
      if($("input[name='MID']:checked").length > midlimit) {
         this.checked = false;         
         alert("You can choose maximum 5 midfielders");
      }
      if($("input[name='FWD']:checked").length > fwdlimit) {
         this.checked = false;         
         alert("You can choose maximum 3 forwards");
      }
      if((($("input[name='GKP']:checked").length) + ($("input[name='DEF']:checked").length) + ($("input[name='MID']:checked").length) + ($("input[name='FWD']:checked").length)) == 15)  {
         document.getElementById("sub").disabled = false;
      }
   });
});