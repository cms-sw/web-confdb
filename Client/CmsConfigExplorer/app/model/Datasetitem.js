Ext.define('CmsConfigExplorer.model.Datasetitem', {
    extend: 'Ext.data.Model',
    
    fields: [
        { name: 'name', type: 'string' }

    ],
    
    proxy: {
        type: 'ajax',
        url : 'alldatasetitems',
        headers: {'Content-Type': "application/json" },
        limitParam: '',
        pageParam: '',
        sortParam: '',
        //extraParams: {'itype':'{selectedPathitem.pit}'},
        startParam : '',
        reader: {
            type: 'json',
            rootProperty: 'children'
        }
//        lazyFill: true
    }
});
