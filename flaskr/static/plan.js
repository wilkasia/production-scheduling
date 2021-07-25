require([
    'dojo/dom',
    'dojo/dom-construct',
    'dojo/dom-style',
    'dojo/on',
    'dojo/query',
    'dojo/json',
    'dojo/ready',
    'dojo/domReady!'
],function (dom,domConstruct,domStyle,on,query,JSON,ready) {
    'use strict';

    ready(function () {


        on(dom.byId('add-item'),'click',function (){

            const dItems = dom.byId('div-items');
            const sType = dom.byId('s-type');
            const sTonnage = dom.byId('s-tonnage');
            console.log(sType);

            const iDiv = domConstruct.create('div',{style:{margin:'2px 0 2px 0'}});
            const iType = domConstruct.create('input',{type:'text',value:sType[sType.selectedIndex].innerHTML,readonly:'readonly'},iDiv);
            domConstruct.create('span',{class:'space-x2'},iDiv);
            const iTonage = domConstruct.create('input',{type:'text',style:{width:'100px'}},iDiv);
            domConstruct.create('span',{class:'space-x2'},iDiv);
            const iDelete = domConstruct.create('i',{class:'fa fa-window-close fa-lg app-shadow', style:{color:'red'}},iDiv);
            let iInput = domConstruct.create('input',{type:'hidden',name:'items[]', value:''},iDiv);

            on(iTonage,'change',function (){
                iInput.value = JSON.stringify({id:sType.value,tonnage:this.value});
            });

            on(iDelete,'click',function (){
                domConstruct.destroy(iDiv);
            });

            iTonage.value = '0';

            domConstruct.place(iDiv,dItems);
        })
    });

});