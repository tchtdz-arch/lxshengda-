// ===== 中英文切换 =====
// 英文站（/en/）通过 window.LX_FORCE_LANG 锁定为英文，不受 localStorage 影响
var currentLang = (function(){
  if(typeof window!=='undefined' && window.LX_FORCE_LANG) return window.LX_FORCE_LANG;
  try{return localStorage.getItem('lang')||'zh';}catch(e){return 'zh';}
})();
function applyLang(lang){
  currentLang = lang;
  try{localStorage.setItem('lang',lang);}catch(e){}
  var en = lang==='en';
  document.documentElement.lang = en?'en':'zh-CN';
  // 页面标题与描述
  var titleEl = document.querySelector('meta[name="og:title"]');
  var tEl = document.querySelector('title');
  if(tEl){
    if(tEl.getAttribute('data-zh')!==null){
      tEl.textContent = en ? tEl.getAttribute('data-en') : tEl.getAttribute('data-zh');
    }
  }
  var descEl = document.querySelector('meta[name="description"]');
  if(descEl && descEl.getAttribute('data-zh')!==null){
    descEl.setAttribute('content', en ? descEl.getAttribute('data-en') : descEl.getAttribute('data-zh'));
  }
  // 文本内容
  document.querySelectorAll('[data-zh]').forEach(function(el){
    var v = el.getAttribute(en?'data-en':'data-zh');
    if(v!==null){el.innerHTML = v;}
  });
  // placeholder
  document.querySelectorAll('[data-zh-ph]').forEach(function(el){
    var v = el.getAttribute(en?'data-en-ph':'data-zh-ph');
    if(v!==null){el.setAttribute('placeholder',v);}
  });
  // 语言按钮
  var btn = document.getElementById('langToggle');
  if(btn){btn.textContent = en?'中文':'EN';}
  // 年份
  var y = new Date().getFullYear();
  document.querySelectorAll('#year').forEach(function(s){s.textContent=y;});
}
var langToggleEl = document.getElementById('langToggle');
// 英文站的「中文」是跳转链接，不再做原地切换
if(langToggleEl && !window.LX_FORCE_LANG){
  langToggleEl.addEventListener('click',function(){
    applyLang(currentLang==='zh'?'en':'zh');
  });
}

// 移动端菜单
var toggle=document.getElementById('navToggle'),nav=document.getElementById('mainNav');
if(toggle && nav){
  toggle.addEventListener('click',function(){nav.classList.toggle('open');});
}

// 询价表单 → 邮件（仅首页有该表单）
var inquiryForm = document.getElementById('inquiryForm');
if(inquiryForm){
  inquiryForm.addEventListener('submit',function(e){
    e.preventDefault();
    var name=document.getElementById('fName').value.trim();
    var company=document.getElementById('fCompany').value.trim();
    var phone=document.getElementById('fPhone').value.trim();
    var email=document.getElementById('fEmail').value.trim();
    var product=document.getElementById('fProduct').value;
    var msg=document.getElementById('fMsg').value.trim();
    var body='客户称呼：'+name+'\n公司名称：'+company+'\n联系电话：'+phone+'\n电子邮箱：'+email+'\n咨询产品：'+product+'\n需求描述：'+msg;
    var subject='网站询价 - '+name+' - '+product;
    // 询价统一发往 Gmail（页面已不再展示 163，且海外送达率更好）
    var mailTo = 'sales@lxshengda.com';
    window.location.href='mailto:'+mailTo+'?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);
    alert(currentLang==='en'
      ? 'An inquiry email has been prepared. If your email client does not open automatically, please send it manually to '+mailTo+'.'
      : '已为您生成询价邮件，如未自动调起邮箱客户端，请手动发送至 '+mailTo+'。');
  });
}

// 灯箱
function openLightbox(src, el){
  var img=document.getElementById('lightboxImg');
  var cap=document.getElementById('lightboxCap');
  var box=document.getElementById('certLightbox');
  if(!img||!box)return;
  img.src=src;
  if(cap){cap.textContent=(el?el.getAttribute(currentLang==='en'?'data-en-cap':'data-zh-cap'):'')||'';}
  box.classList.add('open');
  document.body.style.overflow='hidden';
}
function closeLightbox(e){
  var box=document.getElementById('certLightbox');
  if(!box)return;
  if(e && e.target && e.target.tagName==='IMG')return;
  box.classList.remove('open');
  document.body.style.overflow='';
}
document.addEventListener('keydown',function(e){
  if(e.key==='Escape'){var box=document.getElementById('certLightbox');if(box){box.classList.remove('open');document.body.style.overflow='';}}
});

// 初始化语言
applyLang(currentLang);
