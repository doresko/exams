function whenAceLoaded(){
    if(typeof ace === "undefined"){
        //do nothing
    } else {
        clearTimeout(cb);
        document.getElementById("id_text").style.display = "none";
        var editor = ace.edit("editor");
        editor.getSession().setMode("ace/mode/python");
        if(localStorage.getItem('theme') == "dark"){editor.setTheme("ace/theme/dracula");}
        if(localStorage.getItem('theme') == "light"){editor.setTheme("ace/theme/xcode");}

        function Submit() {
        document.getElementById('id_text').value = editor.getValue();
        }
    }
}

var cb;
window.onload = function(){
    var cb = this.setTimeout( function() {whenAceLoaded()}, 100);
}
