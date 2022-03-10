<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import {ref} from 'vue'
import * as PIXI from 'pixi.js'
import {round, solveWithBackend, PointData} from './utils'

const radius = 3;
let app: PIXI.Application | null = null;

let mouseState = {
  inState: false,
  curPos: {x: ref(0), y: ref(0)},
  lastClickPos: {x: 0, y: 0},
  pressPos: {x: 0, y: 0},
  releasePos: {x: 0, y: 0}
}

let problem = {
  distance: ref(-1),
  indicator: new PIXI.Graphics(), // remember add indicator to app.stage

  clear(){
    this.indicator.clear();
  },

  setAnswerPair(x1: number, y1: number, x2:number, y2: number){
    let dis = Math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2));
    this.distance.value = dis;

    this.indicator.clear();
    this.indicator.lineStyle({
      color: 0xff5050,
      width: 3
    })
    this.indicator.moveTo(x1, y1);
    this.indicator.lineTo(x2, y2);
  }
}

interface PointState{
  selected: boolean;
}
class MyPoint{
  state: PointState;
  g: PIXI.Graphics;
  group: MyPoint[];

  constructor(g: PIXI.Graphics, group: MyPoint[]){
    this.state = {selected: false};
    this.g = g;
    this.draw(0);
    this.group = group;

    g.buttonMode = true;
    g.interactive = true;
    g.hitArea = new PIXI.Circle(0, 0, radius);
    g.on("click", () => {this.toggleSelection()})
  }

  toggleSelection(){
    if(this.state.selected) this.unselect()
    else this.select();
  }

  draw(color: number){
    let g = this.g;
    g.clear();
    g.beginFill(color);
    g.drawCircle(0, 0, radius);
    g.endFill();
  }

  select() {
    this.state.selected = true;
    this.draw(0xFF0000);

    // for(let p of this.group){
    //   if(p == this) continue;
    //   p.unselect();
    // }
  }

  unselect(){
    this.state.selected = false;
    this.draw(0);
  }

  deleteSelf(){
    this.g.destroy();
    app?.stage.removeChild(this.g);
  }
}

let pointList: MyPoint[] = []

const inputCountStr = ref("10");
const inputCountInvalid = ref(false);
const inputCountMsg = ref("");
function inputCountValidator(event: any) {
  let value = event.target.value;
  if (!/^\+?[1-9][0-9]*$/.test(value)) {
    inputCountInvalid.value = true;
    inputCountMsg.value = "NOT AN POSITIVE INTEGER!";
  }else{
    inputCountInvalid.value = false;
  }
}

let solveProblem = function(){
  let u = -1, v = -1, a = 1e9;
  for(let i = 0;i < pointList.length;i++){
    let x1 = pointList[i].g.x;
    let y1 = pointList[i].g.y;
    for(let j = i+1;j < pointList.length;j++){
      let x2 = pointList[j].g.x;
      let y2 = pointList[j].g.y;
      let dis2 = (x1-x2) * (x1-x2) + (y1-y2)*(y1-y2);
      if(dis2 < a){
        a = dis2;
        u = i;
        v = j;
      }
    }
  }
  if(u >= 0){
    problem.setAnswerPair(
      pointList[u].g.x,
      pointList[u].g.y,
      pointList[v].g.x,
      pointList[v].g.y
    );

    pointList.forEach((p) => p.unselect())
    pointList[u].select();
    pointList[v].select();
  }else{
    problem.clear();
  }
}

function addPoint(x:number, y: number){
  if(app == null){ return ;}

  let g  = new PIXI.Graphics();
  g.x = x;
  g.y = y;
  app.stage.addChild(g);

  let p = new MyPoint(g, pointList);
  pointList.push(p);

  solveProblem();
}

function deleteSelectedPoints(){
  let list = pointList.filter((p) => p.state.selected);
  pointList = pointList.filter((p) => !p.state.selected);

  list.forEach((p) => p.deleteSelf());
  solveProblem();
}

function initPixi(){
  app = new PIXI.Application({
      backgroundColor: 0xffffff,
      width: 600,
      height: 600
  });
  let viewContainer = document.getElementById("stage");

  if(viewContainer){
      while(viewContainer.children.length){
          let x = viewContainer.children.item(0);
          if(x) viewContainer.removeChild(x);
      }
      viewContainer.appendChild(app.view);
      app.view.addEventListener("contextmenu", function(e){e.preventDefault()})
  }

  app.stage.hitArea = new PIXI.Rectangle(0, 0, 600, 600);
  app.stage.interactive = true

  // 位置显示
  let crossIndicator = new PIXI.Graphics();
  crossIndicator.lineStyle({
    color: 0x30ff6b,
    width: 1
  });
  crossIndicator.moveTo(-20, 0); crossIndicator.lineTo(20, 0);
  crossIndicator.moveTo(0, -20); crossIndicator.lineTo(0, 20);
  app.stage.addChild(crossIndicator);
  app.stage.on("pointerdown", function(event: PIXI.InteractionEvent){
    mouseState.pressPos.x = event.data.global.x;
    mouseState.pressPos.y = event.data.global.y;
  });
  app.stage.on("pointerup", function(event: PIXI.InteractionEvent){
    let x = event.data.global.x;
    let y = event.data.global.y;
    mouseState.releasePos.x = x;
    mouseState.releasePos.y = y;

    if(event.data.button == 2) {
      addPoint(x, y);
    }
  });
  app.stage.on("pointermove", function(event: PIXI.InteractionEvent){
    if(mouseState.inState){
      mouseState.curPos.x.value = round(event.data.global.x, 2);
      mouseState.curPos.y.value = round(event.data.global.y, 2);
      crossIndicator.position.x = event.data.global.x;
      crossIndicator.position.y = event.data.global.y;
    }
  })
  app.stage.on("pointerover", () => {mouseState.inState = true;});
  app.stage.on("pointerout", ()=>{mouseState.inState = false;});

  // 图形边界
  let boundary = new PIXI.Graphics();
  boundary.lineStyle({color: 0xFF0000, width: 1})
  boundary.drawRect(1, 1, 599, 598);
  app.stage.addChild(boundary);

  // 答案指示器
  app.stage.addChild(problem.indicator);
}

function generatePoints(){
  if(app == null) return;
  let count = parseInt(inputCountStr.value);
  if(count > 1000){
    inputCountInvalid.value = true;
    inputCountMsg.value = "TOO BIG.";
    return;
  }

  pointList.forEach((p) => p.deleteSelf());
  pointList = []

  // monkey patch solveProblem
  const oldFunc = solveProblem;
  solveProblem = function(){};

  while(count--){
    addPoint(Math.random() * app.stage.width, Math.random() * app.stage.height);
  }
  
  // restore solveProblem
  solveProblem = oldFunc;
  solveProblem();
}

let netState = ref("");
let bckSolveResult = ref({})
function computeByBackend(){
  let p: PointData[] = []
  pointList.forEach((e) => {p.push({x: e.g.x, y: e.g.y})})
  netState.value = "Sent request..."
  document.getElementById("cmpByBckBtn")?.setAttribute("disabled", "disabled");
  solveWithBackend(p).then((ans) => {
    bckSolveResult.value = ans;
    netState.value = "Done.."
  })
  .catch(() => netState.value = "!!! error !!!")
  .finally(() => document.getElementById("cmpByBckBtn")?.removeAttribute("disabled"));
}

function generateByBackend(){
  netState.value = "Sent request...";
  document.getElementById("genByBckBtn")?.setAttribute("disabled", "disabled");
  fetch(`/api/genandsolve?n=${inputCountStr.value}`)
    .then((res) => res.json())
    .then((json) => {
      bckSolveResult.value = json;
      netState.value = "Done..";
    })
    .catch((e) => {
      netState.value = "!!! error !!!";
      console.log(e)
    })
    .finally(() => document.getElementById("genByBckBtn")?.removeAttribute("disabled"));
}

</script>
 
<template>
<div style="display:flex; flex-direction: row;">
  <div id="stage">
      <button v-on:click="initPixi" style="width: 100%; height: 100%; background-color: lightgray;">Click here to start.</button>
  </div>
  <div id="info">
      <span>Mouse Point: ({{mouseState.curPos.x}}, {{mouseState.curPos.y}}) </span>
      <span>Distance: {{problem.distance}}</span>

      <button v-on:click="deleteSelectedPoints" style="align-self: baseline;">Delete Point</button>

      <div>
        Count: <input v-model="inputCountStr" v-on:keyup="inputCountValidator($event)"/> <br/>
        <span v-if="inputCountInvalid" style="color: red;">{{inputCountMsg}}</span> <br/>
        <button v-on:click="generatePoints">Random Points</button>
      </div>

      <div style="height: 20px;"></div>

      <div style="margin-left: 10">
        <button id="cmpByBckBtn" v-on:click="computeByBackend" style="display: inline-block;">Solve By Backend</button>
        <button id="genByBckBtn" v-on:click="generateByBackend" style="margin-left: 20px;">Generate And Solve By Backend</button>
        <br/>
        <span>{{netState}}</span>
        <ul style="width: 600px;overflow: auto;white-space: nowrap;">
          <li v-for="(value, key) in bckSolveResult" style="margin-bottom: 10px">
            {{key}}: <br/>
            time: {{value["time"]}} s, dis: {{value["dis"]}}, 
            ({{value["point"]["u"]["x"]}}, {{value["point"]["u"]["y"]}}) -- ({{value["point"]["v"]["x"]}}, {{value["point"]["v"]["y"]}})
          </li>
        </ul>
      </div>
  </div>
</div>
<br/>
使用说明：
<ol>
  <li>左侧是显示区域，鼠标右键新建点，左键选择点，被选择的点显示为红色。</li>
  <li>“Count”输入框中点的个数用于设置随机生成点的数目。</li>
  <li>“Random Points”在前端生成随机的点，要求点的数量不大于1000，前端使用 n^2 算法确定最近点对。</li>
  <li>“Solve By Backend”将前端生成的点发送到后端，通过Python计算最近点对。</li>
  <li>“Generate...”后端随机生成“Count”个点，并计算最近点对，这里不限制点的数量。</li>
  <li>后端运行结果说明：<ul>
    <li>brute：使用n^2算法</li>
    <li>solve：使用nlog(n)算法</li>
    <li>其他：表示在nlog(n)算法递归到点的数量小于等于30时，直接n^2计算最近点对时，使用的排序算法。builtin 表示Python自带的排序算法。</li>
  </ul></li>
</ol>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
}

#stage {
  margin-right: 10px;
  width: 604px;
  height: 604px;
  border: solid 1px black;
  padding: 2px;
  display: flex;
  justify-content: center;
  align-items: center;
}

#stage canvas {
  cursor: none !important;
}

#info {
  display: flex;
  flex-direction: column;
  text-align: left;
}
</style>
