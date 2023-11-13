var treePath = "";
var zTreeObj = "";
var hidObj ="";
var valueObj="";  
var menuContent = "";
var setting = {};

function onClick(e,treeId, treeNode) {
	var zTree = $.fn.zTree.getZTreeObj(zTreeObj);
	if(treeNode.isParent){
		var level = treeNode.level;
		if(level>0){
			$("#" + hidObj).attr("value", treeNode.id);
			$("#" + valueObj).val(treeNode.name);
			hideMenu();
		}
	}else{
		$("#" + hidObj).attr("value", treeNode.id);
		$("#" + valueObj).val(treeNode.name);
		hideMenu();
	}
}

function onDblClick(event, treeId, treeNode){
	$("#" + hidObj).val(treeNode.id);
	if($("#" + valueObj).length>0){
		$("#" + valueObj).val(treeNode.name);
	}else{
		$("#" + hidObj).val(treeNode.name);
	}
	hideMenu();
}

var treeCombox;
function showMenu(config) {
	treePath = rootUrl+config.treePath;
	zTreeObj = config.hidObj+"_zTreeObj";
	hidObj =config.hidObj;
	valueObj=config.hidObj+"_NAME";
	menuContent = config.hidObj+"_MenuContent";
	setting = {
  view: {
    dblClickExpand: true,
    selectedMulti: false,
    showLine: true
  },
  async: {
    enable: true,
    url: treePath,
    autoParam: ["id=id"],
    contentType : "application/json",
    headers: {
      "Content-Type": "application/json"
    }
  },
  callback : {
    onClick: onClick
    // ,onDblClick: onDblClick
  }
};
	treeCombox = $.fn.zTree.init($("#"+zTreeObj), setting);
	var pidObj = $("#" + valueObj);
	var pidOffset = $("#" + valueObj).offset();
	if(!(pidObj.length>0)){
		pidObj = $("#"+hidObj);
		pidOffset = $("#"+hidObj).offset();
	}
	$("#"+menuContent).css({
		left : pidOffset.left + "px",
		top : pidOffset.top + pidObj.outerHeight() + "px"
	}).slideDown("fast");
	$("body").bind("mousedown", onBodyDown);
}
function hideMenu() {
	$("#"+menuContent).fadeOut("fast");
	$("body").unbind("mousedown", onBodyDown);
}
function onBodyDown(event) {
	if (!(event.target.id == "menuBtn" || event.target.id == menuContent || $(
			event.target).parents("#"+menuContent).length > 0)) {
		hideMenu();
	}
}
