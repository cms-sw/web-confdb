Ext.define('CmsConfigExplorer.model.Sequenceitem', {
    extend: 'Ext.data.Model',

    fields: [
        { name: 'name', type: 'string' },
        { name: 'pit', type: 'string' }

    ],
    
    proxy: {
        type: 'ajax',
        url : 'allseqitems',
        timeout : 480000,
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
