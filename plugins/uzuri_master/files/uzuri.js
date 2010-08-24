var current_plugin = [];
var current_host = "";

function load_remote(id, url)
{
    var xmlReq = null;
    if(window.XMLHttpRequest)
	xmlReq = new XMLHttpRequest();
    else if(window.ActiveXObject)
	xmlReq = new ActiveXObject("Microsoft.XMLHTTP");
    if(xmlReq==null) return; // Failed to create the request

    xmlReq.id = id;
    show_host_status(id, "active");

    xmlReq.onreadystatechange = function()
    {
        if (xmlReq.readyState == 4)
        {
	    id = xmlReq.id;
	    if (xmlReq.status == 200) {
		obj = document.getElementById("remote-" + id);
		obj.innerHTML = xmlReq.responseText;
		try {
		    oo = obj.getElementsByClassName("ui-el-mainwindow-right")[0]
		    obj.innerHTML = oo.innerHTML
		} catch (err) { }
		eval_scripts(obj);
		show_host_status(id, "idle");

		try {
		    current_plugin[id] = xmlReq.getResponseHeader("X-Uzuri-Plugin");
		    highlight_currents();
		} catch (err) { }

	    } else {
		show_host_status(id, "error");
	    }
        }
    }

    xmlReq.open ("GET", url, true);
    xmlReq.send (null);
    return false;
}

function eval_scripts(obj)
{
    var ob = obj.getElementsByTagName("script");
    for(var i=0; i<ob.length-1; i++)
        try {
            if(ob[i+1].text!=null) eval(ob[i+1].text);
        } catch (err) {}
}


function show_host_status(id, st)
{
    if (st == "idle")
	ui_show(id + "-icon-idle");
    else
	ui_hide(id + "-icon-idle");

    if (st == "active")
	ui_show(id + "-icon-active");
    else
	ui_hide(id + "-icon-active");

    if (st == "error")
	ui_show(id + "-icon-error");
    else
	ui_hide(id + "-icon-error");

    if (st == "warning")
	ui_show(id + "-icon-warning");
    else
	ui_hide(id + "-icon-warning");
}

function switch_host(id)
{
    var x = document.getElementById("uzuri-mainpane");
    for (i=0; i<x.children.length; i++)
	if (x.children[i].id != id)
	    ui_hide(x.children[i].id);
    ui_show(id);
    current_host = id.split('-')[2];
    highlight_currents();
}

function switch_host_num(num)
{
    var x = document.getElementById("uzuri-mainpane");
    for (i=0; i<x.children.length; i++)
	if (i == num) {
	    ui_show(x.children[i].id);
	    current_host = x.children[i].id.split('-')[2];
	} else
	    ui_hide(x.children[i].id);
    if (num == -1)
	current_host = "all";
    highlight_currents();
}

function highlight_currents()
{
    var x = document.getElementById("uzuri-sidepane");
    for (i=0; i<x.children.length; i++) {
	e = x.children[i];
	if (e.className == "uzuri-remote-plugin-button-active")
	    e.className = "uzuri-remote-plugin-button";
	if (e.className == "uzuri-remote-host-button-active")
	    e.className = "uzuri-remote-host-button";
	if (e.id == ("plugin-" + current_plugin[current_host]))
	    e.className = "uzuri-remote-plugin-button-active";
	if (e.id == ("remotebtn-" + current_host))
	    e.className = "uzuri-remote-host-button-active";
	if (e.id == "remoteallbtn" && current_host == "all")
	    e.className = "uzuri-remote-host-button-active";
    }
}

function execute_query(url)
{
}