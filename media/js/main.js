function reply(msg_id,user_id,user){
	var Title = document.getElementById("title");
	var Message = document.getElementById("message");
	var Msg_id = document.getElementById("msg_id");
	var User_id = document.getElementById("user_id");
	var T = document.getElementById("title_" + msg_id);
	if(T){
		Title.value = T.innerHTML;
	}
	Message.value = "@" + user + " ";
	Message.focus();
	Msg_id.value = msg_id
	User_id.value = user_id
}

function add_title(title){
	var Title = document.getElementById("title");
	var Message = document.getElementById("message");
	Title.value = title;
	Message.focus();
}

function quote(user,date,id){
	var ACstring = document.getElementById("content_" + id).innerHTML;
	var AcComment = document.getElementById("message");
	AcComment.value = "引用 " + user + " 在 " + date + "的发言:\n" + SetChineseString(ACstring,128) + "\n-----\n";
	AcComment.focus();
}

function SetChineseString(str,len)
{
	var strlen = 0; 
	var s = "";
	for(var i = 0;i < str.length;i++)
	{
	if(str.charCodeAt(i) > 128){
			strlen += 2;
			}else{ 
			strlen++;
		}
		s += str.charAt(i);
		if(strlen >= len){ 
		return s + "..." ;
		}
	}
 	return s;
 }
 
function Refresh()
{
var xmlhttp=new XMLHttpRequest();
xmlhttp.onreadystatechange=function()
  {
  if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
	var div = document.createElement("DIV");
	var text = document.createTextNode(xmlhttp.responseText);
	div.appendChild(text);
	var list = document.getElementById("chatList");
    list.appendChild(div);
    }
  }
xmlhttp.open("GET","/refresh/?t=" + Math.random(),true);
xmlhttp.send();
t=setTimeout("Refresh()",30000);
}


$(document).ready(function() {
	// $("#refresh").click(function() {
	$(this).everyTime("60s",function() {
		var last = $("#chatList ul li:first").attr("id");
		$.getJSON("/refresh/", { last_msg_id: last },  function(data) {
			$("li.last-new-msg").removeClass("last-new-msg");
			$.each(data, function(key, val) {
				var id = val['id'];
				var user_id = val['user_id'];
				var name = val['username'];
				var avatar = val['avatar'];
				var title = val['title'];
				var message =  val['content'];
				var time =  val['date'];
				var fav_num = val['fav_num'];
				if (key == 0)
				{
				var content = '<li id="' + id + '" class="clearit last-new-msg">';
				}
				else
				{
				var content = '<li id="' + id + '" class="clearit">';
				}
				content += '<div class="icon ll"><img src="' + avatar + '" class="avatar" align="absmiddle" /></div>';
				content += '<div class="bubble">';
				content += '<div class="msg-header"><span class="screen-name">' + name + '</span></div>';
				content += '<div id="content_' + id + '" class="content">' + message + '</div>';
				content += '<div class="time"><span class="timestamp">' + time + '</span>';
				content += '<a title="Reply" id="reply_num" class="reply-action" href="javascript:reply(' + id + ',' + user_id + ',\'' + name + '\');"><b>回复</b></a> ';
				content += '<a title="Quote" id="quote_num" class="quote-action" href="javascript:quote(\'' + name + '\',\'' + time + '\',' + id + ');"><b>引用</b></a> ';
				content += '<a title="Fav" id="fav_num" class="fav-action" href="/fav/?msg_id=' + id + '"><b>收藏</b></a></div>';
				content += '</div></li>';
				$("#chatList ul").prepend(content);
			});
			//var name = data[0]["fields"]["username"];
			//$("#chatList").prepend(name);
		});
	});
});

// window.onload=Refresh();