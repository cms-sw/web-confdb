Ext.define('CmsConfigExplorer.view.editor.EditorController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.editor-editor',

    onExportedsLoad: function( store, records, successful, eOpts ){
        var det = records[0];
        var urlString = det.get("url");
        
        window.location = urlString;
        
        var loading = this.lookupReference('loadingtext');
        loading.setHidden(true);
        
        var loadinggif = this.lookupReference('loadinggif');
        loadinggif.setHidden(true)
        
        var expbutton = this.lookupReference('exportbutton');
        expbutton.enable();
        
        store.removeAll();
//        
//        console.log('getCount()');
//        console.log(store.getCount().toString());
    
    },
    
    onExportClick: function(){
        
        var cid = this.getViewModel().get("idCnf");        
        var vid = this.getViewModel().get("idVer");
        var online = this.getViewModel().get("online");
        
        var expbutton = this.lookupReference('exportbutton');
        expbutton.disable();
        
        var loading = this.lookupReference('loadingtext');
        loading.setHidden(false);
        
        var loadinggif = this.lookupReference('loadinggif');
        loadinggif.setHidden(false);
        
        var storeExp = this.getViewModel().getStore('exported');
        storeExp.load({params: {cnf: cid, ver: vid, online: online}});
       
    },
    
    onBeforeRender: function(view){
        
        Ext.Ajax.setTimeout(240000);
        
        var cid = this.getViewModel().get("idCnf");        
        var vid = this.getViewModel().get("idVer");
        
        var online = this.getViewModel().get("online");
        
        this.getViewModel().getStore('cnfdetails').load({params: {cnf: cid, ver: vid, online: online}});
        var sumv = view.lookupReference('summaryview');
        var detv = view.lookupReference('detailsview');
        
        sumv.getViewModel().set('idCnf',cid);
        sumv.getViewModel().set('idVer',vid);
        sumv.getViewModel().set('online',online);
        
        detv.getViewModel().set('idCnf',cid);
        detv.getViewModel().set('idVer',vid);
        detv.getViewModel().set('online',online);
        
        var editToll = this.lookupReference('editTool');
        var exportButton = editToll.items.getAt(8); 
        
        if(online == 'file'){
            exportButton.disable();
        }
        
//        var link = window.location.origin + "#menu/" + vid + "_" + online;
        
//        var link = window.location.origin + "#config=" + vid + "_" + online;
//
//        this.getViewModel().set('link',link);
        
//        console.log('getTimeout( ): '+Ext.Ajax.getTimeout().toString());
        
    },
    
    onHomeClick: function(){
            //console.log("In Editor controller");
            var view = this.getView();
            view.fireEvent('backHome');
    },
    
    onExploreClick: function(){
            //console.log("In Editor controller");
            var view = this.getView();
            view.fireEvent('exploreDatabase');
    },
    
    onCnfDetailsLoad: function( store, records, successful, eOpts ){
        var det = records[0];
        var name = det.get("name");
        this.getViewModel().set( "cnfname", name );
        
        var link = window.location.origin + window.location.pathname + "#config=" + name;
        this.getViewModel().set('link',link);
        
        var toolb = this.lookupReference('editTool');
        toolb.add({
            text: 'External link',
            url: link,
//            baseParams: {
//                q: 'html+anchor+tag'
//            },
            tooltip: 'Link to this configuration'
        });
        
    },
    
    onDetailsClick: function( button, e, eOpts ){
        var view = this.lookupReference('cardspanel');
        var sumButton = this.lookupReference('summarybutton');
        var cards = view.getLayout();
        
        var pathtab = this.lookupReference('detailsview').lookupReference('pathtab');
        pathtab.fireEvent('cusDetailsClick');
        
        var moduleTab = this.lookupReference('detailsview').lookupReference('moduleTab');
        moduleTab.fireEvent('loadModules');
        
        button.disable();
        sumButton.enable();
        cards.setActiveItem(1);
        
    },
    
    onSummaryClick: function( button, e, eOpts ){
        var view = this.lookupReference('cardspanel');
        var detButton = this.lookupReference('detailsbutton');
        var cards = view.getLayout();
        button.disable();
        detButton.enable();
        cards.setActiveItem(0);
        
    },
    
    onLinkClick: function(button){
        
        var link = this.getViewModel().get('link');
        
        window.location = link;
        
//        Ext.toast({
//            html: 'Data Saved',
//            slideInDuration: 400,
//            slideBackDuration: 800,
//            hideDuration: 300,
//            autoCloseDelay: 1000,
//            header: false,
////            title: 'My Title',
//            width: 300,
//            align: 't'
//        });

        
    }
    
    
});