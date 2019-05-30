/**
 * Created by Administrator on 2015/6/3.
 */


$(document).ready(function () {

    $('#register').click(function () {
        $('.zhuce').css({'display': 'inherit' });
        $('#ly').css({'display': 'block' });

    })
    $('.zjdl').click(function () {
        $('.zhuce').css({'display': 'inherit' });
        $('#ly').css({'display': 'block' });

    })
    $('#closeReg').click(function () {
        $('.zhuce').css({'display': 'none' });
        $('#ly').css({'display': 'none' });

    })

    $('#searchInput').click(function () {
        $('.tiaok').css({'display': 'block' });
    })

    $('.tiaok1-a1').click(function (e) {
        $(e.target).parent().hide();
    });

    epflag = 0;
    $("#ep").blur(function () {
        epflag = 0;
        tmp = $("#ep").val();
        if (tmp.match(/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/)) {
            epflag = 1;
        }
        else if (tmp.match(/^1\d{10}$/)) {
            epflag = 2;
        }
        else {
            $('#eperror').text('请输入正确的邮箱或手机号');
            $('#ep').css({'border-color': 'red' });
        }
        if (epflag > 0) {
            $('#eperror').text('');
        }
    });
    pwflag = 0
    $("#pw").blur(function () {
        pwflag = 0
        if (!$("#pw").val().match(/^(?=.*?[a-zA-Z])(?=.*?[0-6])[!"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~A-Za-z0-9]{6,16}$/)) {
            $('#pwerror').text('长度为6-16位，至少包含数字和字母');
            $('#pw').css({'border-color': 'red' });
        }
        else {
            $('#pwerror').text('');
            pwflag = 1
            if ($("#pw").val() != $("#pw2").val()) {
                $('#pw2error').text('两次输入的密码不一致');
            }
            else {
                $('#pw2error').text('');
                pw2flag = 1
            }
        }
    });
    pw2flag = 0
    $("#pw2").blur(function () {
        pw2flag = 0
        if ($("#pw").val() != $("#pw2").val()) {
            $('#pw2error').text('两次输入的密码不一致');
            $('#pw2').css({'border-color': 'red' });
        }
        else {
            $('#pw2error').text('');
            pw2flag = 1
        }
    });

    $("#ep").focus(function () {
        $("#ep").css({'border-color': '#CCCCCC' });
    });
    $("#pw").focus(function () {
        $("#pw").css({'border-color': '#CCCCCC' });
    });
    $("#pw2").focus(function () {
        $("#pw2").css({'border-color': '#CCCCCC' });
    });
    $("#yzm").focus(function () {
        $("#yzm").css({'border-color': '#CCCCCC' });
        $("#yzmerror").text('')
    });
    $("#reg").click(function () {
        if (epflag + pwflag + pw2flag >= 3) {
            if ($('#xy').attr('checked') == 'checked') {
                $('#xyerror').text('');
//                  $("#regform").submit();
                $.ajax({
                    cache: true,
                    type: "POST",
                    url: "../register/",
                    data: {
                        ep: $("#ep").val(),
                        password: $("#pw").val(),
                        yzm: $("#yzm").val(),
                        login_name: '',
                        login_pw: ''
                    },//$('#regform').serialize(),// 你的formid
                    async: true,
                    error: function (request) {
                        alert("Connection error");
                    },
                    success: function (data) {
                        if (data != '验证码错误') {
                            window.location.href = data
                        }
                        else {
                            $("#yzmerror").text(data)
                            $('#yzm').css({'border-color': 'red' });
                        }

                    }
                });
//                    $.post("../register/",
//                      {
//                        ep:$("#ep").val(),
//                        password:$("#pw").val(),
//                        yzm:$("#yzm").val()
//                      },
//                      function(data, status, xhr){
//                          alert(data)
//
//                      });

            }
            else {
                $('#xyerror').text('还未接受龙搜用户协议');
            }
        }
        else {
            $('#xyerror').text('请输入正确的信息');
            if (!epflag) {
                $('#ep').css({'border-color': 'red' });
            }
            if (!pwflag) {
                $('#pw').css({'border-color': 'red' });
            }
            if (!pw2flag) {
                $('#pw2').css({'border-color': 'red' });
            }
        }
    });

    $("#djjh").click(function () {
        $("#jhform").submit();
    })

    $("#finish").click(function () {

        $.post(window.location.href,
            {
                name: $("#name").val(),
                gender: $("#gender").val(),
                sel_Province: $("#sel_Province  option:selected").text(),
                sel_City: $("#sel_City  option:selected").text(),
                sel_County: $("#sel_County  option:selected").text()
            },
            function (data) {
                ajaxobj = eval("(" + data + ")");
                window.location.href = ajaxobj.url
                login_user = ajaxobj.user
            });
    })

    $("#login_pw").focus(function () {
        $("#login_pw").val('');
        $("#login_error").text('');
    });


    login_user = ""
    $("#loginclick").click(function () {
        if ($("#login_name").val() && $("#login_pw").val()) {

            $.post("../login/",
                {
                    login_name: $("#login_name").val(),
                    login_pw: $("#login_pw").val()
                },
                function (data) {
                    if (data == '登录失败') {
                        //alert(data)
                        $("#login_error").text('您输入的帐号或密码有误');

                    }
                    else if (data == '账号未激活') {
                        $("#login_error").html('您输入的帐号尚未激活,<a href="#" id="rejh">现在激活</a>');
                        $("#rejh").click(function () {
                            window.location.href = '../email_reg/?resend=y&email=' + $("#login_name").val();
                        })
                    }
                    else {

                        ajaxobj = eval("(" + data + ")");
                        window.location.href = ajaxobj.url
                        login_user = ajaxobj.user
                    }

                });
        }
        else {
            $("#login_error").text('帐号和密码不能为空');
        }


    })
    if (login_user) {
        $("#login_user").text(login_user);
    }


    $("#fasong1").click(function () {
        e()
    })

    $('#fasong2').click(function () {
        $('.shurkk').css({'display': 'block' });

    })

    $("#radio_enter").click(function () {
        $("#textarea").attr("onkeydown", "keySend2(event);");
    });
    $("#radio_ctrl").click(function () {
        $("#textarea").attr("onkeydown", "keySend(event);");
    });

    $(".shu4").mouseover(function () {
        $(".wl_faces_box").show()
    }).mouseout(function () {
        $(".wl_faces_box").hide()
    }), $(".wl_faces_box").mouseover(function () {
        $(".wl_faces_box").show()
    }).mouseout(function () {
        $(".wl_faces_box").hide()
    }), $(".wl_faces_close").click(function () {
        $(".wl_faces_box").hide()
    }), $(".wl_faces_main img").click(function () {
        var a = $(this).attr("src");
        $("#textarea").val($("#textarea").val() + "*#" + a.substr(a.indexOf("img2/") + 5, 6) + "#*"), $("#textarea").focusEnd(), $(".wl_faces_box").hide()
    })

    $('#right_hide').click(function () {
        if ($(".ss2-y").css("display") != 'none') {
            $('.ss2-y').css({'display': 'none' });
            $('.ss2-z').css({'width': '1366px' });
        }
        else {
            $('.ss2-y').css({'display': 'block' });
            $('.ss2-z').css({'width': '1100px' });
        }

    })

    $("#xyb").click(function () {
        $('#fp1').submit();
    });

    $("#xyb2").click(function () {
        $('#fp2').submit();
    });

    $("#xyb3").click(function () {
        $('#fp3').submit();
    });

    $("#send_yzm").click(function () {
        $.get('../fp2/?resend=y&email=' + $("#fp2name").text());
    });

    $("#ra1").click(function () {
        $("#ra1").css({'background': 'url(../static/img/tiao.png) no-repeat', 'background-position': '17px 0px'});
        $("#ra2").css({'background': ''});
        $("#ra3").css({'background': ''});
        $("#r1").fadeIn(500);
        // $("#r1").show();
        $("#r2").fadeOut(300);
        $("#r3").fadeOut(300);
    });
    $("#ra2").click(function () {
        $("#ra2").css({'background': 'url(../static/img/tiao.png) no-repeat', 'background-position': '17px 0px'});
        $("#ra1").css({'background': ''});
        $("#ra3").css({'background': ''});
        $("#r2").fadeIn(500);
        $("#r1").fadeOut(300);
        $("#r3").fadeOut(300);
    });
    $("#ra3").click(function () {
        $("#ra3").css({'background': 'url(../static/img/tiao.png) no-repeat', 'background-position': '17px 0px'});
        $("#ra1").css({'background': ''});
        $("#ra2").css({'background': ''});
        $("#r3").fadeIn(500);
        $("#r1").fadeOut(300);
        $("#r2").fadeOut(300);
    });

    $("#fasong3").click(function () {
        if ($(".ss2").css("display") != 'none') {
            chatHide();
        }
        else {
            chatShow();
        }
    });

      $(".shu3").click(function () {
          if ($("#content").css("display") != 'none') {
             $("#content").hide();
        }
        else {
             $("#content").show();
        }

    });
})


$(document).bind('click', function (e) {
    var e = e || window.event; //浏览器兼容性
    var elem = e.target || e.srcElement;
    while (elem) { //循环判断至跟节点，防止点击的是div子元素
        if (elem.id && elem.id == 'searchInput' || elem.id == 'tiaok' || elem.id == 'fasong2') {
            return;
        }
        elem = elem.parentNode;
    }
    $('#tiaok').css('display', 'none'); //点击的不是div或其子元素
    $('.shurkk').css({'display': 'none' });
});

function changeImg() {
    document.getElementById("yzmimg").src = "../code?" + Math.random();
}

function e() {
    function h() {
        -1 != g.indexOf("*#emo_") && (g = g.replace("*#", "<img src='../static/img2/").replace("#*", ".gif'/>"), h())
    }

    var e = new Date, f = "";
    f += e.getFullYear() + "-", f += e.getMonth() + 1 + "-", f += e.getDate() + "  ", f += e.getHours() + ":", f += e.getMinutes() + ":", f += e.getSeconds();
    var g = $("#textarea").val();
    h();
    var i = '<div class="nr-xx"><div class="nr-xxz"><div class="nr-xx1"><a class="tx"> <img src="../static/img/212.png" width="68" height="68"/></a></div><div class="nr-xx3"></div></div><Div class="nr-xx2">' + g + '</Div></div>'
    //var i2 = "<div class='message clearfix'><div class='user-logo'><img src='" + b + "'/>" + "</div>" + "<div class='wrap-text'>" + "<h5 class='clearfix'>\u5f20\u98de</h5>" + "<div>" + g + "</div>" + "</div>" + "<div class='wrap-ri'>" + "<div clsss='clearfix'><span>" + f + "</span></div>" + "</div>" + "<div style='clear:both;'></div>" + "</div>" + "<div class='message clearfix'>" + "<div class='user-logo'>" + "<img src='" + c + "'/>" + "</div>" + "<div class='wrap-text'>" + "<h5 class='clearfix'>" + d + "</h5>" + "<div>" + g + "\u7684\u56de\u590d\u5185\u5bb9</div>" + "</div>" + "<div class='wrap-ri'>" + "<div clsss='clearfix'><span>" + f + "</span></div>" + "</div>" + "<div style='clear:both;'></div>";
    null != g && "" != g ? ($(".div_scroll").append(i), $(".ss-nr1").scrollTop($(".div_scroll").height()), $("#textarea").val("")) : alert("\u8bf7\u8f93\u5165\u804a\u5929\u5185\u5bb9!")
    if (null != g && "" != g) {
        $.post("../chat/",
            {
                chat: g
            },
            function (data) {
                var j = '<div class="nr-tx"><div class= "nr-tx1" ><a class="tx"><img src="../static/img/tx2.png" width="68" height="68"/></a></div><div class="nr-tx3z"><div class="nr-tx3"></div><div class="nr-tx2">' + data + ' </div></div></div > '
                null != data && "" != data ? ($(".div_scroll").append(j), $(".ss-nr1").scrollTop($(".div_scroll").height())) : alert("\u8bf7\u8f93\u5165\u804a\u5929\u5185\u5bb9!")
                if(data.length>15){
                    chatShow();

                }
                else{

                    $('.xiaokx12').text(data)
                    if($('.ss2').css('display')=='none'){
                        $("#textarea").val(g)
                        $('.xiaokx').css({'display': 'block' });
                    }

                }
            });
    }
}

function keySend(event) {
    if (event.ctrlKey && event.keyCode == 13) {
        e()
    }
}
function keySend2(event) {
    if (event.keyCode == 13 && !event.ctrlKey) {
        e()
    }
}

function chatShow() {
    $(document.body).css({
   "overflow-x":"hidden",
   "overflow-y":"hidden"
 });
    $(".ss2").fadeIn(1000);
    //$('.ss2').css({'display': 'block' });
    $('.shura').css({'display': 'block' });
    $(".logo").animate({'margin-top': '50px', 'margin-bottom': '30px'});
    //$('.logo').css({'margin-top': '50px','margin-bottom': '30px' });
    $('.xiaokx').css({'display': 'none' });
    $('.biaoq').css({'display': 'none' });
    $('.foot').css({'position': 'relative' });
    $(".fasong3").css({'background': 'url(../static/img/up.png) no-repeat'});
    $(".ss-nr1").scrollTop($(".div_scroll").height());
}

function chatHide() {
    //$(".ss2").fadeOut();
    $('.ss2').css({'display': 'none' });
    $('.shura').css({'display': 'none' });
    $(".logo").animate({'margin-top': '220px'});
    //$('.logo').css({'margin-top': '220px' });
    $('.biaoq').css({'display': 'block' });
    $('.foot').css({'position': 'absolute' });
    $(".fasong3").css({'background': 'url(../static/img/down.png) no-repeat'});

}