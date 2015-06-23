
Ext.define("Demo110315.view.globalpset.GlobalPsetParamsTree",{
    extend: "Ext.tree.Panel",

    controller: "globalpset-globalpsetparamstree",

    alias: 'widget.gpsetparamstree',
    reference: "gpsetParamsTree",

    bind:{
        // bind store to view model "modules" store
        store:'{gpsetparams}'
//        selection: '{selectedModuleitem}'
    },
    bufferedRenderer: false,
    rootVisible: true,
    useArrows: true,
//    singleExpand: true,
    
    columns: [
        { xtype: 'treecolumn', header: 'Name', dataIndex: 'name', flex: 1 },
        { xtype: 'gridcolumn', header: 'Value', dataIndex: 'value', flex: 1},
        { xtype: 'gridcolumn', header: 'Tracked', dataIndex: 'tracked',renderer: function(v, meta, rec) { var  data = rec.getData(); if (data.tracked == 1){return "tracked"} else {return "untracked"} }},
        { xtype: 'gridcolumn', header: 'Type', dataIndex: 'paramtype' },
        { xtype: 'gridcolumn', header: 'Default', dataIndex: 'default', renderer: function(v, meta, rec) {var  data = rec.getData(); if (data.default == 1){ return "True"} else {return "False"} }}
    ]
});
