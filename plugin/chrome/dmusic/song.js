var re = new RegExp('\\d+','m');
var music_id = re.exec(location.pathname);

var dmusic = document.createElement("a");
dmusic.href = "http://dmusic.sinaapp.com/song/" + music_id;
dmusic.target = "_blank";
dmusic.className = "btn btn-b down-song-btn";
dmusic.innerHTML = '<span class="inner"><i class="icon btn-icon-down"></i><span class="txt">Dmusic</span></span>';

var buttons = document.getElementsByClassName("song-opera")[0];
buttons.appendChild(dmusic);
