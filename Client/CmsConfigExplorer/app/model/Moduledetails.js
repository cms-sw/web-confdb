Ext.define('CmsConfigExplorer.model.Moduledetails', {
    extend: 'CmsConfigExplorer.model.Base',
    
    fields: [
        { name: 'name', type: 'string' },
        { name: 'mt', type: 'string' },
        { name: 'mclass', type: 'string' },
        { name: 'author', type: 'string' }

    ],
    
    proxy: {
        type: 'ajax',
        url : 'moddetails',
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
