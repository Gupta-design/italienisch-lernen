const fs = require("fs");
const html = fs.readFileSync("index.html", "utf8");
const m = html.match(/const WENDUNGEN_DATA\s*=\s*(\[[\s\S]*?\n\];)/);
const WENDUNGEN_DATA = eval("(" + m[1].slice(0, -1) + ")");
const gm = html.match(/const WENDUNGEN_GROUPS\s*=\s*(\[[\s\S]*?\n\];)/);
const WENDUNGEN_GROUPS = eval("(" + gm[1].slice(0, -1) + ")");

function shuffleArr(arr){
  const a = arr.slice();
  for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; }
  return a;
}
const QUIZ_QUESTIONS_PER_CARD = 6;
function buildQuizCard(pool){
  const shuffled = shuffleArr(pool);
  const chosen = shuffled.slice(0, QUIZ_QUESTIONS_PER_CARD);
  return chosen.map(item=>{
    const sameCat = shuffleArr(WENDUNGEN_DATA.filter(w=>w.cat===item.cat && w.de!==item.de));
    let wrongPool = sameCat;
    if(wrongPool.length < 3){
      wrongPool = wrongPool.concat(shuffleArr(WENDUNGEN_DATA.filter(w=>w.de!==item.de && !wrongPool.includes(w))));
    }
    const options = shuffleArr([item, ...wrongPool.slice(0,3)]);
    return { prompt: item.it, answer: item.de, options: options.map(o=>o.de) };
  }).filter(q=>q.options.length>=2);
}

console.log("Total WENDUNGEN_DATA:", WENDUNGEN_DATA.length);
console.log("Groups:", WENDUNGEN_GROUPS.map(g=>g[0]));
WENDUNGEN_GROUPS.forEach(([cat])=>console.log(" -", cat, ":", WENDUNGEN_DATA.filter(w=>w.cat===cat).length));
const uncategorized = WENDUNGEN_DATA.filter(w=>!WENDUNGEN_GROUPS.some(g=>g[0]===w.cat));
console.log("Uncategorized (should be 0):", uncategorized.length, uncategorized.slice(0,5));

let problems = 0;
[...WENDUNGEN_GROUPS.map(g=>g[0]), "alle"].forEach(cat=>{
  const pool = cat==="alle" ? WENDUNGEN_DATA : WENDUNGEN_DATA.filter(w=>w.cat===cat);
  if(pool.length < 4){ console.log(`SKIP ${cat}: pool too small (${pool.length})`); return; }
  for(let i=0;i<50;i++){
    const card = buildQuizCard(pool);
    card.forEach(q=>{
      if(!q.options.includes(q.answer)){ console.log("BUG: answer missing", cat, q); problems++; }
      const uniq = new Set(q.options);
      if(uniq.size !== q.options.length){ console.log("BUG: dup options", cat, q); problems++; }
    });
  }
});
console.log("Total problems:", problems);

const dupIt = WENDUNGEN_DATA.map(w=>w.it).filter((v,i,a)=>a.indexOf(v)!==i);
console.log("Duplicate .it keys (state.words collisions):", [...new Set(dupIt)]);
const dupDe = WENDUNGEN_DATA.map(w=>w.de).filter((v,i,a)=>a.indexOf(v)!==i);
console.log("Duplicate .de values within same cat (could reduce distractor pool, not fatal):", [...new Set(dupDe)].length);
