$(document).ready(function(){        
    $("input[type='checkbox']").on('change', 
    function(evt) {        
        if((($("input[name='out_GKP']:checked").length) + ($("input[name='out_DEF']:checked").length) + ($("input[name='out_MID']:checked").length) + ($("input[name='out_FWD']:checked").length)) < (($("input[name='in_GKP']:checked").length) + ($("input[name='in_DEF']:checked").length) + ($("input[name='in_MID']:checked").length) + ($("input[name='in_FWD']:checked").length))){
            this.checked = false;
            alert("You cannot have more than 15 players in your squad");
        }
        if((($("input[name='out_GKP']:checked").length) + ($("input[name='out_DEF']:checked").length) + ($("input[name='out_MID']:checked").length) + ($("input[name='out_FWD']:checked").length)) > 1){
            this.checked = false;
            alert("You are allowed to make one free transfer.")
        }        
        if($("input[name='out_GKP']:checked").length == 1) {
            if($("input[name='in_DEF']:checked").length > 0){
                this.checked = false;
                alert("Please choose a goalkeeper");
            }
            else if($("input[name='in_MID']:checked").length > 0){
                this.checked = false;
                alert("Please choose a goalkeeper");
            }
            else if($("input[name='in_FWD']:checked").length > 0){
                this.checked = false;
                alert("Please choose a goalkeeper");
            }
        }
        if($("input[name='out_DEF']:checked").length == 1) {
            if($("input[name='in_GKP']:checked").length > 0){
                this.checked = false;
                alert("Please choose a defender");
            }
            else if($("input[name='in_MID']:checked").length > 0){
                this.checked = false;
                alert("Please choose a defender");
            }
            else if($("input[name='in_FWD']:checked").length > 0){
                this.checked = false;
                alert("Please choose a defender");
            }            
        }
        if($("input[name='out_MID']:checked").length == 1) {
            if($("input[name='in_GKP']:checked").length > 0){
                this.checked = false;
                alert("Please choose a midfielder");
            }
            else if($("input[name='in_DEF']:checked").length > 0){
                this.checked = false;
                alert("Please choose a midfielder");
            }
            else if($("input[name='in_FWD']:checked").length > 0){
                this.checked = false;
                alert("Please choose a midfielder");
            }            
        }
        if($("input[name='out_FWD']:checked").length == 1) {
            if($("input[name='in_GKP']:checked").length > 0){
                this.checked = false;
                alert("Please choose a forward");
            }
            else if($("input[name='in_DEF']:checked").length > 0){
                this.checked = false;
                alert("Please choose a forward");
            }
            else if($("input[name='in_MID']:checked").length > 0){
                this.checked = false;
                alert("Please choose a forward");
            }            
        }        
        if((($("input[name='out_GKP']:checked").length) + ($("input[name='out_DEF']:checked").length) + ($("input[name='out_MID']:checked").length) + ($("input[name='out_FWD']:checked").length)) == 1){
            document.getElementById('div1').innerHTML = "<h2><b>Free Transfers : 0</b></h2>";
            // document.getElementById('div2').innerHTML = "<h2><b>Cost: 0 Pts</b></h2>";
        }
        else if((($("input[name='out_GKP']:checked").length) + ($("input[name='out_DEF']:checked").length) + ($("input[name='out_MID']:checked").length) + ($("input[name='out_FWD']:checked").length)) == 0){
            document.getElementById('div1').innerHTML = "<h2><b>Free Transfers : 1</b></h2>";
            // document.getElementById('div2').innerHTML = "<h2><b>Cost: 0 Pts</b></h2>";
        }                                                                
    });
});