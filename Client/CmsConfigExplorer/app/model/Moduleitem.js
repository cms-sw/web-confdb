Ext.define('CmsConfigExplorer.model.Moduleitem', {
    extend: 'Ext.data.Model',
    
    fields: [
        { name: 'moduleId', type: 'int' },
        { name: 'name', type: 'string' },
        { name: 'mit', type: 'string' },
        { name: 'value', type: 'string' },
        { name: 'tracked', type: 'int' },
//        { name: 'default', type: 'int' },
        { name: 'isDefault', type: 'string' },
        { name: 'paramtype', type: 'string' }

    ],
    
    proxy: {
        type: 'ajax',
        url : 'allmoditems',
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
