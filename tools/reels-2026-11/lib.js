const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const lin=(t,a,b)=>cl((t-a)/(b-a));
const eo=x=>1-Math.pow(1-x,3);              // ease out cubic
const eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const back=x=>{const c=1.70158;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const mix=(a,b,k)=>a+(b-a)*k;
const $=s=>document.querySelector(s);
const fmt=n=>Math.round(n).toLocaleString('en-US');
function set(el,o){if(typeof el==='string')el=$(el);for(const k in o){if(k==='o')el.style.opacity=o[k];else if(k==='tf')el.style.transform=o[k];else if(k==='txt')el.textContent=o[k];else el.style[k]=o[k];}}
// frame sequence: frames/<dir>/0001.jpg ... ; await seq(img,dir,t)
async function seq(el,dir,t,fps=30,n=99999){const i=cl(Math.floor(t*fps),0,n-1)+1;const src=`frames/${dir}/${String(i).padStart(4,'0')}.jpg`;if(!el.src.endsWith(src)){el.src=src;try{await el.decode()}catch(e){}}}
