/*
上传图片配置
*/
$.jUploader.setDefaults({
    cancelable: true, // 可取消上传
    allowedExtensions: ['jpg', 'png', 'bmp'], // 只允许上传图片
    messages: {
        upload: '上传',
        cancel: '取消',
        emptyFile: "{file} 为空，请选择一个文件.",
        invalidExtension: "{file} 后缀名不合法. 只有 {extensions} 是允许的.",
        onLeave: "文件正在上传，如果你现在离开，上传将会被取消。"
    }
});
$(function(){
    upload_img();//上传图片
});//function
/*
上传图片方法
 */
var ld_param = {'btn_id': '上传按钮标签id','img_id': '原图标签id', 'parent_div_css': '原图标签外层div样式', 'img_path':'上传提交隐藏域id',
                'cut_size':['剪切此寸列表,4个此寸，最小宽高，最大宽高，注意等比例'], 'width':'原图标签宽度', 'height':'原图标签高度',
                'img_size':[{'img_id':'剪切尺寸标签id', 'x':'剪切尺寸宽度', 'y':'剪切尺寸高度', 'saveBtn_id': '保存按钮id'}]//'img_size列表中多个值代表要剪切出的不同尺寸'
}
var img_path = ''//剪切图片时需要上传图片url;
function upload_img(){
$.jUploader({
    button: ld_param.btn_id, // 这里设置按钮id
    action: '/upload/image?store_dir="user"', // 这里设置上传处理接口，这个加了参数test_cancel=1来测试取消
    // 上传完成事件
    onComplete: function (fileName, response) {
        // response是json对象，格式可以按自己的意愿来定义，例子为： { success: true, fileUrl:'' }
        if (response.success) {
            jcrop_div_width = ld_param.width;//调整剪切框位置(图片在框中位置，需根据设计调整)
            jcrop_div_height = ld_param.height;//调整剪切框位置(图片在框中位置，需根据设计调整)
            $('.'+ld_param.parent_div_css).html('<img src="" id="'+ld_param.img_id+'" style="max-width: '+ld_param.width+'px;max-height: '+ld_param.height+'px;"/>');
            var random = Math.random();
            $('#'+ld_param.img_id).attr('src','/static/photo/users/' + response.file_name+'?'+random).show();
            //$(".jcrop-holder").find('img').attr('src','/c/' + response.file_name);
             // 这里说明一下，一般还会在图片附近加添一个hidden的input来存放这个上传后的文件路径(response.fileUrl)，方便提交到服务器保存
            img_path = '/static/photo/users/' + response.file_name;//剪切图片时需要上传图片url;
            $('#'+ld_param.img_path).val(img_path)
            for(var i=0; i<ld_param.img_size.length; i++){
                $('#'+ld_param.img_size[i].name).attr('src','/static/photo/users/' + response.file_name+'?'+random);
            }
            initJcrop("#"+ld_param.img_id, ld_param.cut_size, showCoords);//调用图片剪切
            $('#'+ld_param.saveBtn_id).show();
        }else {
            alert('上传失败');
        }
    }
    });
}
/*图片剪切方法 */
var jcrop_api;
var img_info1 = {'x':0,'y':0,'x2':0,'y2':0,'w':0,'h':0,'path':''};//剪切图片信息
//图片剪切方法
function initJcrop(obj_img,cut_size,obj_even){
    x = cut_size[0]
    y = cut_size[1]
    x1 = cut_size[2]
    y1 = cut_size[3]
    $(obj_img).Jcrop({
        onChange:   obj_even,
        onRelease: releaseCheck
    },function(){
        jcrop_api = this;
        jcrop_api.animateTo([0,0,x,y]);//大图上切图框大小
        jcrop_api.setOptions({ aspectRatio: x/y });//大图上切图框大小
        jcrop_api.setOptions({ minSize: [ x, y ],maxSize: [ x1, y1 ] });//大图上切图框大小
        jcrop_api.setOptions({ allowSelect: false });
        jcrop_api.focus();
        var bounds = this.getBounds();
        boundx = bounds[0];
        boundy = bounds[1];
    });
};

function releaseCheck(){
  jcrop_api.setOptions({ allowSelect: true });
  jcrop_api.focus();
};

function showCoords(c){//获取小图再大图上相对应的位置坐标及剪切的长宽
    x2 = $('#'+ld_param.img_id).width();
    y2 = $('#'+ld_param.img_id).height();
    img_info1 = {'x':c.x,'y':c.y,'x2':x2,'y2':y2,'w':c.w,'h':c.h,'path':''};
    if (parseInt(c.w) > 0){
        for(var i=0; i<ld_param.img_size.length; i++){
            var rx = ld_param.img_size[i].x / c.w;
            var ry = ld_param.img_size[i].y / c.h;
            $('#'+ld_param.img_size[i].name).css({
              width: Math.round(rx * boundx) + 'px',
              height: Math.round(ry * boundy) + 'px',
              marginLeft: '-' + Math.round(rx * c.x) + 'px',
              marginTop: '-' + Math.round(ry * c.y) + 'px'
            });
        }
    }
};
var num = [];
var img_type = '';  //处理特殊尺寸
function save_img_click(){//保存剪切图片尺寸
    img_info1.path = img_path
    var json_img_info = JSON.stringify(img_info1)
    for(var i=0; i<ld_param.img_size.length; i++){
        num.push(JSON.stringify({'width':ld_param.width,
            'height':ld_param.height,'width1':ld_param.img_size[i].x,
            'height1':ld_param.img_size[i].y}))
    }
    /*
    ajax传送到后台剪切图片数据
    */
    var img_name = ''
    $.ajax({
        type : "post",
        url : "/upload/repics",
        data : {'imgtype':'face', 'img_info':json_img_info, 'num':num},
        async: false,
        success: function(img_name){
            img_name = eval(img_name);
            img_path = img_name[0];//剪切图片时需要上传图片url;
            //$('#'+ld_param.img_path).val(img_path);
            //提交图片路径到后台
            postImgUrl(img_path);
        }
    });
}