const lines=["杂谈 · 静墨","俯仰之间，皆是生活"];
let lineIdx=0,charIdx=0;
const el=document.getElementById('typed');
function type(){
  if(charIdx<lines[lineIdx].length){
    el.textContent+=lines[lineIdx][charIdx++];
    setTimeout(type,120);
  }else{
    setTimeout(()=>{el.textContent="";charIdx=0;
      lineIdx=(lineIdx+1)%lines.length;type();},2000);
  }
}
type();