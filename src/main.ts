import * as PIXI from 'pixi.js'
import Vue from 'vue';

const vueApp = Vue.createApp({
    data: () => {return {
        mouseX: 0, mouseY: 0,
        pointCount: 0,
    }}
})

const vm = vueApp.mount("#info")

const app = new PIXI.Application({
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
}

app.stage.hitArea = new PIXI.Rectangle(0, 0, 600, 600);
app.stage.interactive = true
app.stage.on("pointerup", function(event: PIXI.InteractionEvent){
    
})