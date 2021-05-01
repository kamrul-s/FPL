function create_league(){
    document.getElementById('create_form').style.display = 'block';
    document.getElementById('join_form').style.display = 'none';
    document.getElementById('join').style.display = 'none';
}

function join_league(){
    document.getElementById('join_form').style.display = 'block';
    document.getElementById('create_form').style.display = 'none';
    document.getElementById('create').style.display = 'none';
}