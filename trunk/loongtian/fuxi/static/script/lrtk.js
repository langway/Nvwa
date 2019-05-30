// JavaScript Document
window.onload = function()
{
  var oBox = document.getElementById('box');
  var oPrev = getByClass(oBox,'prev')[0];
  var oNext = getByClass(oBox,'next')[0];
  var oBigUl = getByClass(oBox,'bigUl')[0];
  var aLiBig = oBigUl.getElementsByTagName('li');
  var oNumUl = getByClass(oBox,'numberUl')[0];
  var aLiNumber = oNumUl.getElementsByTagName('li');
  var oTextUl = getByClass(oBox,'textUl')[0];
  var aLiText = oTextUl.getElementsByTagName('li');
  var nowZindex = 1;
  var now = 0;
  function tab()
  {
       for(var i=0; i<aLiNumber.length; i++)
          {
              aLiNumber[i].className = '';
          }
          aLiNumber[now].className = 'night';

      aLiBig[now].style.zIndex = nowZindex++;
      aLiBig[now].style.opacity = 0;
      startMove(aLiBig[now],'opacity',100);
      for(var i=0; i<aLiText.length; i++)
      {
          aLiText[i].style.display = 'none';
      }
      aLiText[now].style.display = 'block'

  }

  for(var i=0; i<aLiNumber.length; i++)
  {
      aLiNumber[i].index = i;
      aLiNumber[i].onclick = function()
      {

          if(this.index==now)return;
          now = this.index;

          tab();
      }
  }
  oNext.onmouseover = oPrev.onmouseover = oBigUl.onmouseover = function()
  {
      startMove(oPrev,'opacity',100);
       startMove(oNext,'opacity',100)
  }
   oNext.onmouseout = oPrev.onmouseout = oBigUl.onmouseout = function()
  {
      startMove(oPrev,'opacity',0);
      startMove(oNext,'opacity',0)
  }
  oPrev.onclick = function()
  {
      now--
      if(now==-1)
      {
          now=aLiNumber.length-1;
      }
      tab();
  }

    oNext.onclick = function()
  {
      now++
      if(now==aLiNumber.length)
      {
          now=0;
      }
      tab();
  }

  var timer = setInterval(oNext.onclick,3000)
  oBox.onmouseover = function()
  {
      clearInterval(timer)
  }
  oBox.onmouseout = function()
  {
      timer = setInterval(oNext.onclick,3000)//改变速度修改3000 ，例如3000=3秒钟
  }
}
function getByClass(oParent,name)
{
	var aClass = oParent.getElementsByTagName('*');
	var arlt = [];
	for(var i=0; i<aClass.length; i++)
	{
		if(aClass[i].className==name)
		{
			arlt.push(aClass[i]);
		}
	}
	return arlt;
}

function getStyle(obj,name)
{
	if(obj.currentStyle)
	{
		return obj.currentStyle[name]
	}
	else
	{
		return getComputedStyle(obj,false)[name]
	}
}

function startMove(obj,styleName,iTarget)
{
	clearInterval(obj.timer)
	obj.timer = setInterval(function(){
          var now = 0;
		  if(styleName=='opacity')
		  {
			  now = Math.round((parseFloat(getStyle(obj,styleName))*100));
		  }
		  else
		  {
			  now = parseInt(getStyle(obj,styleName));
		  }
		  var speed = (iTarget-now)/6;
		  speed = speed>0?Math.ceil(speed):Math.floor(speed);
		  if(now == iTarget)
		  {
			  clearInterval(obj.timer)
		  }
		  else
		  {
			  if(styleName=='opacity')
			  {
				  obj.style.opacity = (now+speed)/100;
				  obj.style.filter = 'alpha(opacity='+(now+speed)+')'
			  }
			  else
			  {
				  obj.style[styleName] = now+speed+'px';
			  }
		  }
	},30)
}