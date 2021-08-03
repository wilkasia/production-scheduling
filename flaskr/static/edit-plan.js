require([
    'dojo/dom',
    'dojo/dom-construct',
    'dojo/dom-style',
    'dojo/on',
    'dojo/json',
    'dojo/request/xhr',
    'dojo/ready',
    'dojo/domReady!'
], function (dom, domConstruct, domStyle, on, JSON, xhr, ready) {
    'use strict';

    ready(function () {

        on(dom.byId('test-btn'), 'click', function () {

            var scheduleTable = document.getElementById('schedule-table');
            var sequence = []

            for (var i = 1; i < scheduleTable.rows.length; i++) {
                var objCells = scheduleTable.rows.item(i).cells;
                for (var j = 4; j < objCells.length - 1; j++) {
                    var cellVal = objCells.item(j).innerHTML;
                    sequence.push(cellVal)
                }
            }

            xhrByObject('/validate-schedule', {sequence : sequence}, function (response) {
                console.log(response);
                if(response.length > 0) {

                    const rd = dom.byId('new-rules-div')
                    domConstruct.create('h2',{innerHTML:'Powstały nowe reguły:'},rd);
                    const td = domConstruct.create('table',{class:'schedule-table'},rd);
                    const tbody = domConstruct.create('tbody',{},td);
                    const trh = domConstruct.create('tr',{},tbody);
                    domConstruct.create('th',{colspan:2,class:'schedule-th',innerHTML:'Nowa reguła'},trh);
                    domConstruct.create('th',{class:'schedule-th',innerHTML:'Dodaj'},trh);

                    response.forEach(function (item) {
                        const rule = {from:item[0],to:item[1]};
                        const tr = domConstruct.create('tr',{class:'schedule-tr'},tbody);
                        domConstruct.create('td',{class:'schedule-td', innerHTML:item[0]},tr);
                        domConstruct.create('td',{class:'schedule-td', innerHTML:item[1]},tr);
                        domConstruct.create('td',{class:'schedule-td', innerHTML:'<input class="new-rule" data-reg='+JSON.stringify(rule)+' type="checkbox">'},tr);
                    })
                }
            });

        });
        
    });

    const xhrByObject = function (url, obj, onOk) {

        xhr(url, {
            method: 'POST',
            handleAs: 'json',
            data: JSON.stringify(obj),
            headers: {'Content-Type': 'application/json'}
        }).then(
            function (response) {
                if (response.message === 'OK') {
                    onOk(response.data);
                }
            },
            function (err) {

                try {
                    console.error(JSON.parse(err.response.text).message);
                } catch (e) {
                    window.location.reload();
                }
            });
    }

    const xhrById = function (url, id, onOk) {
        xhrByObject(url, {id: id}, onOk);
    };

});