require([
    'dojo/dom',
    'dojo/on',
    'dojo/json',
    'dojo/request/xhr',
    'dojo/ready',
    'dojo/domReady!'
], function (dom, on, JSON, xhr, ready) {
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