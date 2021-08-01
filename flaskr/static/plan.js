require([
    'dojo/dom',
    'dojo/dom-construct',
    'dojo/dom-style',
    'dojo/on',
    'dojo/query',
    'dojo/json',
    'dojo/request/xhr',
    'dojo/ready',
    'dojo/domReady!'
],function (dom,domConstruct,domStyle,on,query,JSON,xhr,ready) {
    'use strict';

    ready(function () {


        on(dom.byId('add-item'),'click',function (){

            const dItems = dom.byId('div-items');
            const sType = dom.byId('s-type');
            const sTonnage = dom.byId('s-tonnage');
            console.log(sType);

            const iDiv = domConstruct.create('div',{style:{margin:'2px 0 2px 0'}});
            const iType = domConstruct.create('input',{type:'text',value:sType[sType.selectedIndex].innerHTML,'data-id':sType[sType.selectedIndex].value, readonly:'readonly'},iDiv);
            domConstruct.create('span',{class:'space-x2'},iDiv);
            const iTonage = domConstruct.create('input',{type:'text',style:{width:'100px'}},iDiv);
            domConstruct.create('span',{class:'space-x2'},iDiv);
            const iDelete = domConstruct.create('i',{class:'fa fa-window-close fa-lg app-shadow', style:{color:'red'}},iDiv);
            let iInput = domConstruct.create('input',{type:'hidden',name:'items[]', value:''},iDiv);

            on(iTonage,'change',function (){
                iInput.value = JSON.stringify({id:iType.dataset.id,tonnage:this.value});
            });

            on(iDelete,'click',function (){
                domConstruct.destroy(iDiv);
            });

            iTonage.value = '0';

            domConstruct.place(iDiv,dItems);
        })

        on(dom.byId('test-btn'),'click',function(){

            xhrByObject('/test-ajax',{id:123,name:'jakas nazwa'},function (response){
               console.log(response);
            });

        });
    });

    const xhrByObject = function(url,obj,onOk) {
        // if(wait) {
        //     dcBase.appWait(true);
        // }
        xhr(url, {
            method: 'POST',
            handleAs: 'json',
            data: JSON.stringify(obj),
            headers: { 'Content-Type': 'application/json'}
        }).then(
            function(response){
                //console.log(response);
                if(response.message==='OK') {
                    // if(wait) {
                    //     dcBase.appWait(false);
                    // }
                    onOk(response.data);
                }
            },
            function(err){
                // if(wait) {
                //     dcBase.appWait(false);
                // }
                try {
                    // appMsg.error(JSON.parse(err.response.text).message);
                    console.error(JSON.parse(err.response.text).message);
                } catch (e) {
                    window.location.reload();
                }
            });
    }

    const xhrById = function(url,id,onOk) {
        xhrByObject(url,{id:id},onOk);
    };



});