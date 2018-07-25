Ext.define('CmsConfigExplorer.model.ESSource', {
    extend: 'Ext.data.Model',
    
    fields: [
        { name: 'name', type: 'string' },
        { name: 'tclass', type: 'string' }

    ],
    
    proxy: {
        type: 'ajax',
        url : 'essource',
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
