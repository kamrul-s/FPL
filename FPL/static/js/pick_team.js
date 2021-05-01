$(document).ready(function(){
    var gklimit = 1;
    var def_min = 3;
    var def_max = 5;
    var mid_max = 5;
    var mid_min = 2;
    var fwd_min = 1;
    var fwd_max = 3;
    var player_limit = 11;    
    $("input[type='checkbox']").on('change', 
    function(evt) {        
        if($("input[name='starting_GKP']:checked").length > gklimit) {
          this.checked = false;
          alert("You can start only 1 goalkeeper");
        }        
        if($("input[name='starting_DEF']:checked").length > def_max){
          this.checked = false;
          alert("You cannot start more than 5 defenders");
        }                     
        if($("input[name='MID']:checked").length > mid_max) {               
          alert("You can choose maximum 5 midfielders");
        }                
        if((($("input[name='starting_GKP']:checked").length) + ($("input[name='starting_DEF']:checked").length) + ($("input[name='starting_MID']:checked").length) + ($("input[name='starting_FWD']:checked").length)) >player_limit ){
          this.checked = false;
          alert("You cannot start more than 11 players");
        }  
        if(($("input[name='starting_GKP']:checked").length == 1) && ((($("input[name='starting_MID']:checked").length) + ($("input[name='starting_FWD']:checked").length)) > 7)){        
          this.checked = false;
          alert("You must start at least 3 defenders");
        }
        if(($("input[name='starting_GKP']:checked").length == 1) && ((($("input[name='starting_MID']:checked").length) + ($("input[name='starting_DEF']:checked").length)) > 9)){        
          this.checked = false;
          alert("You must start at least 1 forward");
        }
        if((($("input[name='starting_DEF']:checked").length) + ($("input[name='starting_MID']:checked").length) + ($("input[name='starting_FWD']:checked").length)) > 10 ){
          this.checked = false;
          alert("You must start one goalkeeper");
        }  
        if((($("input[name='starting_GKP']:checked").length) + ($("input[name='starting_DEF']:checked").length) + ($("input[name='starting_MID']:checked").length) + ($("input[name='starting_FWD']:checked").length)) == 11 ){
          document.getElementById("sb").disabled = false;
        }                                              
    });
});

