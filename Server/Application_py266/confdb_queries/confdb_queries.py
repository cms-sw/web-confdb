# File confdb_queries.py Description:
# This files contains the implementations of the methods providing the query 
# to retrieve records from the ConfDb
# 
# Class: ConfDbQueries

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.sql import select
from sqlalchemy.sql import text
from sqlalchemy import Sequence
from operator import attrgetter
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

from confdb_tables.confdb_tables import *
#from sqlalchemy_plugin.saplugin import Version, Pathidconf, Pathids, Paths, Pathitems, Pathelement, Modelement, Moduleitem, ModTelement, ModToTemp, ModTemplate, Directory, Configuration, Moduletypes, 

class ConfDbQueries(object):
    
    #Returns the Sequences Paelements records (Sequences and their Modules) in a given path
    #@params: 
    #         id_version: id of Confversion table in the confDB
    #         id_pathid: id of path_id table in the confDB
    #         db: database session object
    #
    def getCompletePathSequences(self,id_pathid=-2, id_version=-2, db=None):
        
        elements = []
        if (id_pathid == -2 or id_version == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        elements = db.query(Pathelement).from_statement(text("SELECT "
                        + "u_paelements.id, "
                        + "u_paelements.name, "
                        + "u_paelements.paetype "                                       
                        + "FROM u_pathid2pae, u_paelements, u_pathid2conf "
                        + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid " 
                        + "and u_pathid2pae.id_pathid=:node "
                        + "and u_pathid2pae.id_pae=u_paelements.id "
                        + "and ((u_pathid2pae.lvl=0 and u_paelements.paetype=2) or u_pathid2pae.lvl>0) "
                        + "and u_pathid2conf.id_confver=:leng "
                        + "order by u_pathid2pae.id ")).params(node=id_pathid, leng=id_version).all()
        
        return elements
        
        
    #Returns the Sequences Pathitems records (Sequences and their Modules) in a given path
    #@params: 
    #         id_version: id of Confversion table in the confDB
    #         id_pathid: id of path_id table in the confDB
    #         db: database session object
    #
    def getCompletePathSequencesItems(self,id_pathid=-2, id_version=-2, db=None):
        
        items = []
        if (id_pathid == -2 or id_version == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        items = db.query(Pathitems).from_statement(text("SELECT "
                        + "u_pathid2pae.id, "
                        + "u_pathid2pae.id_pathid, "                                      
                        + "u_pathid2pae.id_pae, "                                       
                        + "u_pathid2pae.id_parent,"
                        + "u_pathid2pae.lvl, " 
                        + "u_pathid2pae.ord "                                            
                        + "FROM u_pathid2pae,u_paelements, u_pathid2conf  "
                        + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid " 
                        + "and u_pathid2pae.id_pathid=:node "
                        + "and u_pathid2pae.id_pae=u_paelements.id "
                        + "and ((u_pathid2pae.lvl=0 and u_paelements.paetype=2) or u_pathid2pae.lvl>0) "
                        + "and u_pathid2conf.id_confver=:leng "
                        + "order by u_pathid2pae.id ")).params(node=id_pathid, leng=id_version).all()
        
        return items
        
    
    #Returns the Streamid associated with the output module present in a given End Path
    #@params: 
    #         
    #         id_pathid: id of path_id table in the confDB
    #         db: database session object
    #
    def getOumStreamid(self,id_pathid=-2, db=None):
        
        if (id_pathid == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        oum = db.query(PathidToOutM).from_statement(text("SELECT DISTINCT "
                        + "u_pathid2outm.id, "
                        + "u_pathid2outm.id_pathid, " 
                        + "u_pathid2outm.id_streamid, "                                       
                        + "u_pathid2outm.ord "                                           
                        + "FROM u_pathid2outm "
                        + "WHERE u_pathid2outm.id_pathid=:node ")).params(node=id_pathid).first()
        
        return oum
    
    #Returns the Stream from the streamid for an End Path
    #@params: 
    #         
    #         id_pathid: id of path_id table in the confDB
    #         db: database session object
    #
    def getStreamid(self,id_streamid=-2, db=None):
        
        if (id_streamid == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        stid = db.query(StreamId).from_statement(text("SELECT DISTINCT "
                        + "u_streamids.id, u_streamids.id_stream "                   
                        + "FROM u_streamids "
                        + "WHERE u_streamids.id=:node ")).params(node=id_streamid).first()
        
        return stid
    
    
    #Returns the Pathitems records (Modules) present in the level 0 of a given Path
    #@params: 
    #         id_version: id of Confversion table in the confDB
    #         id_pathid: id of path_id table in the confDB
    #         db: database session object
    #
    def getLevelZeroPathItems(self,id_pathid=-2, id_version=-2, db=None):
        
        items = []
        if (id_pathid == -2 or id_version == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        items = db.query(Pathitems).from_statement(text("SELECT "
                        + "u_pathid2pae.id, "
                        + "u_pathid2pae.id_pathid, " 
                        + "u_pathid2pae.id_pae, "                                       
                        + "u_pathid2pae.id_parent,"
                        + "u_pathid2pae.lvl, " 
                        + "u_pathid2pae.ord "                                           
                        + "FROM u_pathid2pae,u_paelements, u_pathid2conf  "
                        + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid " 
                        + "and u_pathid2pae.id_pathid=:node "
                        + "and u_pathid2pae.id_pae=u_paelements.id "
                        + "and (u_pathid2pae.lvl=0 and u_paelements.paetype!=2) "
                        + "and u_pathid2conf.id_confver=:leng "
                        + "order by u_pathid2pae.id ")).params(node=id_pathid, leng=id_version).all()
        
        return items
    
    
    
    #Returns the level zero Paelements records (Modules) in a given path
    #@params: 
    #         id_version: id of Confversion table in the confDB
    #         id_pathid: id of path_id table in the confDB
    #         db: database session object
    #
    def getLevelZeroPaelements(self,id_pathid=-2, id_version=-2, db=None):
        
        elements = []
        if (id_pathid == -2 or id_version == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        elements = db.query(Pathelement).from_statement(text("SELECT "
                        + "u_paelements.id, "
                        + "u_paelements.name, "
                        + "u_paelements.paetype "                                       
                        + "FROM u_pathid2pae, u_paelements, u_pathid2conf "
                        + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid " 
                        + "and u_pathid2pae.id_pathid=:node "
                        + "and u_pathid2pae.id_pae=u_paelements.id "
                        + "and (u_pathid2pae.lvl=0 and u_paelements.paetype!=2) "
                        + "and u_pathid2conf.id_confver=:leng "
                        + "order by u_pathid2pae.id ")).params(node=id_pathid, leng=id_version).all()
        
        return elements    
    
    
    #Returns the Version from the id
    #@params: 
    #         id_ver: id of ConfVersion table in the confDB
    #         db: database session object
    #
    def getVersion(self,id_ver=-2, db=None):
        
        if (id_ver == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        version = db.query(Version).get(id_ver)
        
        return version

    #Returns the paths of a given ConfVersion
    #@params: 
    #         id_version: id of ConfVersion table in the confDB
    #         db: database session object
    #
    def getPaths(self,id_version=-2, db=None):
        
        pats = []
        if (id_version == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        pats = db.query(Pathids).from_statement(text("SELECT u_pathids.id, u_pathids.id_path, u_pathids.isendpath "
                      + "FROM  u_pathids, u_pathid2conf "
                      + "WHERE u_pathids.id = u_pathid2conf.id_pathid "
                      + "AND u_pathid2conf.id_confver=:idv AND u_pathids.isEndPath = 0 order by u_pathid2conf.ord")).params(idv=id_version).all()
        
        return pats
    
    #Returns the END paths of a given ConfVersion
    #@params: 
    #         id_version: id of ConfVersion table in the confDB
    #         db: database session object
    #
    def getEndPaths(self,id_version=-2, db=None):
        
        pats = []
        if (id_version == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        pats = db.query(Pathids).from_statement(text("SELECT u_pathids.id, u_pathids.id_path, u_pathids.isendpath "
                      + "FROM  u_pathids, u_pathid2conf "
                      + "WHERE u_pathids.id = u_pathid2conf.id_pathid "
                      + "AND u_pathid2conf.id_confver=:idv AND u_pathids.isEndPath = 1 order by u_pathid2conf.ord")).params(idv=id_version).all()
        
        return pats
    
    
    def getPathName(self,id_pathid=-2, id_ver=-2,db=None):
        
        if (id_pathid == -2 or db == None or id_ver==-2):
            print ("PARAMETERS EXCEPTION HERE")
            
        patname = db.query(Paths).from_statement(text("SELECT u_paths.id, u_paths.name "
                      + "FROM  u_pathids, u_pathid2conf, u_paths "
                      + "WHERE u_pathids.id = u_pathid2conf.id_pathid "
                      + "AND u_pathids.id_path = u_paths.id "   
                      + "AND u_pathids.id=:id_pid "                                       
                      + "AND u_pathid2conf.id_confver=:idv ")).params(idv=id_ver, id_pid=id_pathid).first()
        
        return patname
    
    
    #Returns the template from the module (Paelement) id
    #@params: 
    #         id_pae: id of Paelement table in the confDB
    #         db: database session object
    #
    def getTemplateFromPae(self,id_pae=-2, db=None):
        
        if (id_pae == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        template_id = db.query(ModToTemp).filter(ModToTemp.id_pae==id_pae).first()
        print "TID:" ,template_id.id_templ
        template = db.query(ModTemplate).filter(ModTemplate.id==template_id.id_templ).first()
        
        return template
    
    def getTemplateParams(self,id_templ=-2, db=None):
        
        if (id_templ == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        tempelements = db.query(ModTelement).filter(ModTelement.id_modtemp==id_templ).all()  
        
        return tempelements
    
    def getModuleParamItems(self,id_pae=-2, db=None):
        
        if (id_pae == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")

#        q = db.query(Moduleitem).from_statement(text("SELECT DISTINCT u_pae2moe.id, u_pae2moe.id_pae, u_pae2moe.id_moe, u_pae2moe.lvl, u_pae2moe.ord "               
#        + "FROM u_pae2moe INNER JOIN (" 
#        + " SELECT MAX(u_pae2moe.id) maxid, u_pae2moe.id_pae, u_pae2moe.id_moe "
#        + " FROM u_pae2moe GROUP BY u_pae2moe.id_moe, u_pae2moe.id_pae ) myPae2Moe "           
#        + "ON u_pae2moe.id = myPae2Moe.maxid AND myPae2Moe.id_pae =:id_pae")).params(id_pae=id_pae)
        
        q = db.query(Moduleitem).from_statement(text("SELECT DISTINCT u_pae2moe.id, u_pae2moe.id_pae, u_pae2moe.id_moe, u_pae2moe.lvl, u_pae2moe.ord "               
        + "FROM u_pae2moe INNER JOIN (" 
        + " SELECT MAX(u_pae2moe.id) maxid, u_pae2moe.id_pae, u_pae2moe.id_moe "
        + " FROM u_pae2moe WHERE u_pae2moe.id_pae =:id_pae GROUP BY u_pae2moe.id_moe, u_pae2moe.id_pae ORDER BY u_pae2moe.id_moe) myPae2Moe "           
        + "ON u_pae2moe.id = myPae2Moe.maxid ORDER BY u_pae2moe.id_moe")).params(id_pae=id_pae)
    
        print "QUERY: ", str(q)
        items = q.all()     
        
#        else:
#            items = db.query(Moduleitem).from_statement(text("SELECT DISTINCT u_pae2moe.id, u_pae2moe.id_pae, u_pae2moe.id_moe, u_pae2moe.lvl, u_pae2moe.ord "
#            + "FROM u_pae2moe, u_pathid2pae "
#            + "WHERE u_pae2moe.id_pae =:id_pae "
#            + "AND u_pathid2pae.id_pae = u_pae2moe.id_pae "
#            + "AND u_pathid2pae.id_pathid =:id_pid "                                                 
#            + "ORDER BY u_pae2moe.id_moe")).params(id_pae=id_pae, id_pid=id_pathid).all()  
        
        return items
    
    def getModuleParamElements(self,moeIds=None, db=None):

        if (moeIds==None or db == None):
                print ("PARAMETERS EXCEPTION HERE")

        elements = db.query(Modelement).filter(Modelement.id.in_(moeIds)).order_by(Modelement.id).all()  

        return elements
    
    
    def getAllDirectories(self,db=None):

        if (db == None):
                print ("PARAMETERS EXCEPTION HERE")

        directories = db.query(Directory).all() 

        return directories 
    
    def getDirectoryByName(self,name="",db=None):

        if (db == None or name==""):
                print ("PARAMETERS EXCEPTION HERE")

        directory = db.query(Directory).filter(Directory.name == name).first()

        return directory 
    
    def getConfigsInDir(self,id_parent=-2,db=None):

        if (db == None or id_parent == -2):
                print ("PARAMETERS EXCEPTION HERE")

        configs = db.query(Configuration).from_statement(text("SELECT  u_configurations.id, u_configurations.name FROM u_configurations, u_confversions WHERE u_configurations.id = u_confversions.id_config and u_confversions.id_parentdir=:id_par")).params(id_par=id_parent).all()

        return configs 
    
    def getConfVersions(self,id_config=-2,db=None):

        if (db == None or id_config == -2):
                print ("PARAMETERS EXCEPTION HERE")

        versions = db.query(Version).filter(Version.id_config == id_config).all()

        return versions
    
    def getModToTempByPae(self,id_pae=-2,db=None):

        if (db == None or id_pae == -2):
                print ("PARAMETERS EXCEPTION HERE")

        mod2temp = db.query(ModToTemp).filter(ModToTemp.id_pae==id_pae).first()

        return mod2temp
    
    def getMod2TempByPaelemets(self,id_paes=None,db=None):

        if (db == None or id_paes == None):
                print ("PARAMETERS EXCEPTION HERE")

        mod2temps = db.query(ModToTemp).filter(ModToTemp.id_pae.in_(id_paes)).all()

        return mod2temps
    
    def getMod2TempByVer(self,id_ver=None,db=None):

        if (db == None or id_ver == None):
                print ("PARAMETERS EXCEPTION HERE")

        mod2temps = db.query(ModToTemp).from_statement(text("SELECT UNIQUE u_mod2templ.id, u_mod2templ.id_pae, u_mod2templ.id_templ "
						+ "FROM u_pathid2pae,u_paelements, u_pathid2conf, u_mod2templ "
						+ "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid "
						+ "and u_pathid2pae.id_pae=u_paelements.id "
						+ "and u_paelements.paetype=1 "
						+ "and u_mod2templ.id_pae=u_paelements.id "
						+ "and u_pathid2conf.id_confver=:ver")).params(ver = id_ver).all()

        return mod2temps
    
    
    def getTempIdByPae(self,id_pae=-2,db=None):

        if (db == None or id_pae == -2):
                print ("PARAMETERS EXCEPTION HERE")

        mod2temps = db.query(ModToTemp.id_templ).filter(ModToTemp.id_pae==id_pae).first()

        return mod2temps[0]
    
    def getModTemplate(self,id_temp=-2,db=None):

        if (db == None or id_temp == -2):
                print ("PARAMETERS EXCEPTION HERE")

        modTemp = db.query(ModTemplate).filter(ModTemplate.id==id_temp).first()

        return modTemp
    
    def getPaelement(self,id_pae=-2,db=None):

        if (db == None or id_pae == -2):
                print ("PARAMETERS EXCEPTION HERE")

        element = db.query(Pathelement).get(id_pae)

        return element
    
    def getConfPaelements(self,id_ver=-2,db=None):

        if (db == None or id_ver == -2):
                print ("PARAMETERS EXCEPTION HERE")

        elements = db.query(Pathelement).from_statement(text("SELECT UNIQUE u_paelements.id, u_paelements.name "
						+ "FROM u_pathid2pae,u_paelements, u_pathid2conf " #, u_mod2templ
						+ "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid "
						+ "and u_pathid2pae.id_pae=u_paelements.id "
						+ "and u_paelements.paetype=1 "
#						+ "and u_mod2templ.id_pae=u_paelements.id "
						+ "and u_pathid2conf.id_confver=:ver order by u_paelements.name")).params(ver = id_ver).all()

        return elements
    
    
    def getRelTemplates(self,id_rel=-2,db=None):

        if (db == None or id_rel == -2):
                print ("PARAMETERS EXCEPTION HERE")

        templates = db.query(ModTemplate).from_statement(text("select u_moduletemplates.id, u_moduletemplates.name, "
						+ " u_moduletemplates.id_mtype "
						+ "from u_moduletemplates, u_modt2rele "
						+ "where u_modt2rele.id_release=:id_rel "
						+ "and u_modt2rele.id_modtemplate=u_moduletemplates.id ")).params(id_rel=id_rel).all()

        return templates
    
    def getAPathidByPae(self,id_rel=-2,db=None):

        if (db == None or id_rel == -2):
                print ("PARAMETERS EXCEPTION HERE")

        templates = db.query(ModTemplate).from_statement(text("select u_moduletemplates.id, u_moduletemplates.name, "
						+ " u_moduletemplates.id_mtype "
						+ "from u_moduletemplates, u_modt2rele "
						+ "where u_modt2rele.id_release=:id_rel "
						+ "and u_modt2rele.id_modtemplate=u_moduletemplates.id ")).params(id_rel=id_rel).all()

        return templates
    
    
    def getConfServices(self,id_ver=-2,db=None):

        if (db == None or id_ver == -2):
                print ("PARAMETERS EXCEPTION HERE")

        elements = db.query(Service).from_statement(text("SELECT UNIQUE u_services.id, u_services.id_template, u_conf2srv.ord "
						+ "FROM u_services, u_conf2srv "
						+ "WHERE u_conf2srv.id_service = u_services.id "
						+ "AND u_conf2srv.id_confver=:ver order by u_conf2srv.ord")).params(ver = id_ver).all()

        return elements
    
    
    def getConfPrescale(self,id_ver=-2, id_templ=-2, db=None):

        if (db == None or id_ver == -2 or id_templ == -2):
                print ("PARAMETERS EXCEPTION HERE")

        elements = db.query(Service).from_statement(text("SELECT UNIQUE u_services.id, u_services.id_template, u_conf2srv.ord "
						+ "FROM u_services, u_conf2srv "
						+ "WHERE u_conf2srv.id_service = u_services.id "
                        + "AND u_services.id_template=:id_templ "
						+ "AND u_conf2srv.id_confver=:ver order by u_conf2srv.ord")).params(ver = id_ver, id_templ=id_templ).first()

        return elements
    
    def getConfPrescaleTemplate(self,id_rel=-2,db=None):

        if (db == None or id_rel == -2):
                print ("PARAMETERS EXCEPTION HERE")

        prescaleTemplate = db.query(SrvTemplate).from_statement(text("SELECT u_srvtemplates.id, u_srvtemplates.name "
						+ "FROM u_srvtemplates, u_srvt2rele "
						+ "WHERE u_srvt2rele.id_release=:id_rel "
                        + "AND u_srvtemplates.name=:name "
						+ "AND u_srvt2rele.id_srvtemplate=u_srvtemplates.id ")).params(id_rel=id_rel,name="PrescaleService").first()

        return prescaleTemplate
    
    def getRelSrvTemplates(self,id_rel=-2,db=None):

        if (db == None or id_rel == -2):
                print ("PARAMETERS EXCEPTION HERE")

        templates = db.query(SrvTemplate).from_statement(text("SELECT u_srvtemplates.id, u_srvtemplates.name "
						+ "FROM u_srvtemplates, u_srvt2rele "
						+ "WHERE u_srvt2rele.id_release=:id_rel "
						+ "AND u_srvt2rele.id_srvtemplate=u_srvtemplates.id ")).params(id_rel=id_rel).all()

        return templates
    
    
    def getSrvTemplateBySrv(self,sid=-2,db=None):

        if (db == None or sid == -2):
                print ("PARAMETERS EXCEPTION HERE")

        template = db.query(SrvTemplate).from_statement(text("SELECT u_srvtemplates.id, u_srvtemplates.name "
						+ "FROM u_srvtemplates, u_services "
						+ "WHERE u_services.id_template=u_srvtemplates.id "
                        + "AND u_services.id=:sid")).params(sid=sid).first()

        return template
    
    def getSrvTemplateParams(self,id_templ=-2, db=None):
        
        if (id_templ == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        tempelements = db.query(SrvTempElement).filter(SrvTempElement.id_srvtemplate==id_templ).all()  
        
        return tempelements
    
    def getServiceParamElements(self,srvId=None, db=None):

        if (srvId==None or db == None):
                print ("PARAMETERS EXCEPTION HERE")

        elements = db.query(SrvElement).filter(SrvElement.id_service == srvId).order_by(SrvElement.id).all()  

        return elements
    
    
    
    def getConfStreams(self,ver=-2,db=None):

        if (db == None or ver == -2):
                print ("PARAMETERS EXCEPTION HERE")

#        streams = db.query(StreamId).from_statement(text("SELECT DISTINCT u_streamids.id, u_streamids.id_stream "
#						+ "FROM u_streamids,u_EVENTCONTENTIDS,u_EVCO2STREAM,u_pathid2outm,u_pathid2conf,u_conf2evco "
#						+ "WHERE u_EVCO2STREAM.id_evcoid=u_EVENTCONTENTIDS.ID "
#						+ "AND u_EVCO2STREAM.ID_STREAMID=u_streamids.id "
#						+ "AND u_streamids.id=u_pathid2outm.id_streamid "
#						+ "AND u_conf2evco.id_confver=u_pathid2conf.id_confver "
#						+ "AND u_conf2evco.id_evcoid=u_EVENTCONTENTIDS.ID "
#						+ "AND u_pathid2conf.id_pathid=u_pathid2outm.id_pathId "
#						+ "AND u_pathid2conf.id_confver =:ver ")).params(ver=ver).all()

        streams = db.query(StreamId).from_statement(text("SELECT DISTINCT u_streamids.id, u_streamids.id_stream "
						+ "FROM u_streamids, u_EVENTCONTENTIDS, u_EVCO2STREAM, u_conf2evco "
						+ "WHERE u_EVCO2STREAM.id_evcoid=u_EVENTCONTENTIDS.ID "
						+ "AND u_EVCO2STREAM.ID_STREAMID=u_streamids.id "
						+ "AND u_conf2evco.id_confver=:ver "
						+ "AND u_conf2evco.id_evcoid=u_EVENTCONTENTIDS.ID")).params(ver=ver).all()

        return streams
    
    def getConfDatasets(self,ver=-2,db=None):

        if (db == None or ver == -2):
                print ("PARAMETERS EXCEPTION HERE")

#        datasets = db.query(DatasetId).from_statement(text("SELECT DISTINCT u_datasetids.id, u_datasetids.id_dataset "
#						+ "FROM u_pathid2strdst, u_pathid2conf,u_datasetids,u_streamids,u_evco2stream, u_conf2evco "
#						+ "WHERE u_pathid2strdst.id_pathid=u_pathid2conf.id_pathid "
#						+ "and u_datasetids.id=u_pathid2strdst.id_datasetid "
#						+ "and u_streamids.id=u_pathid2strdst.id_streamid "
#						+ "and u_evco2stream.id_streamid=u_streamids.id "
#						+ "and u_evco2stream.id_evcoid=u_conf2evco.id_evcoid "
#						+ "and u_conf2evco.id_confver=u_pathid2conf.id_confver "
#						+ "AND u_pathid2conf.id_confver =:ver ")).params(ver=ver).all()


#BUONAAAAA
#        datasets = db.query(DatasetId).from_statement(text("SELECT DISTINCT u_datasetids.id, u_datasetids.id_dataset "
#						+ "FROM u_pathid2strdst, u_datasetids, u_streamids, u_evco2stream, u_conf2evco "
#						+ "WHERE u_datasetids.id=u_pathid2strdst.id_datasetid "
#						+ "and u_streamids.id=u_pathid2strdst.id_streamid "
#						+ "and u_evco2stream.id_streamid=u_streamids.id "
#						+ "and u_evco2stream.id_evcoid=u_conf2evco.id_evcoid "
#						+ "and u_conf2evco.id_confver=:ver ")).params(ver=ver).all()
        
        datasets = db.query(DatasetId).from_statement(text("SELECT DISTINCT u_datasetids.id, u_datasetids.id_dataset "
						+ "FROM u_conf2strdst, u_datasetids "
						+ "WHERE u_datasetids.id=u_conf2strdst.id_datasetid "
						+ "and u_conf2strdst.id_confver=:ver ")).params(ver=ver).all()    
        
#        datasets = db.query(DatasetId).from_statement(text("SELECT DISTINCT u_datasetids.id, u_datasetids.id_dataset "
#                        + "FROM u_conf2strdst, u_datasetids "
#                        + "WHERE u_datasetids.id=u_conf2strdst.id_datasetid "
#                        + "and u_conf2strdst.id_confver=:ver")).params(ver=ver).all()

        return datasets
    
    
    def getConfStrDatRels(self,ver=-2,db=None):
        if (db == None or ver == -2):
                print ("PARAMETERS EXCEPTION HERE")

#        rels = db.query(PathidToStrDst).from_statement(text("SELECT DISTINCT u_pathid2strdst.id, u_pathid2strdst.id_pathid, u_pathid2strdst.id_streamid, u_pathid2strdst.id_datasetid "
#						+ "FROM u_pathid2strdst, u_pathid2conf,u_datasetids,u_streamids,u_evco2stream, u_conf2evco "
#						+ "WHERE u_pathid2strdst.id_pathid=u_pathid2conf.id_pathid "
#						+ "and u_datasetids.id=u_pathid2strdst.id_datasetid "
#						+ "and u_streamids.id=u_pathid2strdst.id_streamid "
#						+ "and u_evco2stream.id_streamid=u_streamids.id "
#						+ "and u_evco2stream.id_evcoid=u_conf2evco.id_evcoid "
#						+ "and u_conf2evco.id_confver=u_pathid2conf.id_confver "
#						+ "AND u_pathid2conf.id_confver =:ver ")).params(ver=ver).all()
#
#        return rels
        
        rels = db.query(ConfToStrDat).from_statement(text("SELECT DISTINCT u_conf2strdst.id, u_conf2strdst.id_confver, u_conf2strdst.id_streamid, u_conf2strdst.id_datasetid "
						+ "FROM u_conf2strdst "
						+ "WHERE u_conf2strdst.id_confver =:ver ")).params(ver=ver).all()

        return rels
  
    def getDatasetPathids(self,ver=-2, dstid =-2 ,db=None):

        if (db == None or ver == -2 or dstid == -2 ):
                print ("PARAMETERS EXCEPTION HERE")

#        pathids = db.query(Pathids).from_statement(text("SELECT distinct u_pathids.id "                             
#                        + "FROM u_pathid2strdst, u_pathid2conf,u_datasetids,u_datasets,u_streams,u_streamids, u_evco2stream, u_conf2evco "
#						+ "WHERE u_pathid2strdst.id_pathid=u_pathid2conf.id_pathid "
#                        + "and  u_pathids.id= u_pathid2conf.id_pathid "                                
#						+ "and  u_datasets.id=u_datasetids.id_dataset "
#						+ "and u_datasetids.id=u_pathid2strdst.id_datasetid "
#						+ "and u_streams.id=u_streamids.id_stream "
#						+ "and u_streamids.id=u_pathid2strdst.id_streamid "
#						+ "AND u_evco2stream.id_streamid=u_streamids.id "
#						+ "and u_evco2stream.id_evcoid=u_conf2evco.id_evcoid "
#						+ "and u_conf2evco.id_confver=u_pathid2conf.id_confver "
#						+ "and u_pathid2conf.id_confver =:ver ")).params(ver=ver).all()
#
#        return pathids

        pathids = db.query(Pathids).from_statement(text("SELECT distinct u_pathids.id "                  
                        + "FROM u_pathid2strdst, u_conf2strdst, u_pathids " 
                        + "WHERE u_conf2strdst.id_confver=:ver "
                        + "and u_pathids.id = u_pathid2strdst.id_pathid "                                
						+ "and u_conf2strdst.id_datasetid=:dstid "
						+ "and u_conf2strdst.id_datasetid=u_pathid2strdst.id_datasetid ")).params(ver=ver, dstid = dstid).all()

        return pathids

    
    
    def getConfEventContents(self,ver=-2,db=None):

        if (db == None or ver == -2):
                print ("PARAMETERS EXCEPTION HERE")

        print "VER: ",ver        
                
        evcontents = db.query(EventContentId).from_statement(text("select U_EVENTCONTENTIDS.id , U_EVENTCONTENTIDS.id_evco "
				+ "from U_EVENTCONTENTIDS, U_CONF2EVCO "
				+ "where U_CONF2EVCO.ID_EVCOID=U_EVENTCONTENTIDS.id " 
                + "and U_CONF2EVCO.id_confver=:ver")).params(ver=ver).all()
        
        return evcontents
    
    
    def getEvCoToStream(self,ver=-2,db=None):

        if (db == None or ver == -2):
                print ("PARAMETERS EXCEPTION HERE")

        relEvCoToStr = db.query(EvCoToStream).from_statement(text("SELECT DISTINCT u_EVCO2STREAM.id, u_EVCO2STREAM.id_streamid, u_EVCO2STREAM.id_evcoid "
						+ "FROM u_EVENTCONTENTIDS,u_EVCO2STREAM,u_conf2evco "
						+ "WHERE u_EVCO2STREAM.id_evcoid=u_EVENTCONTENTIDS.ID "
                        + "AND u_conf2evco.id_evcoid=u_EVENTCONTENTIDS.ID "             
						+ "AND u_conf2evco.id_confver=:ver ")).params(ver=ver).all()

        return relEvCoToStr 
    
    
    def getEvCoStatements(self,evc=-2,db=None):

        if (db == None or evc == -2):
                print ("PARAMETERS EXCEPTION HERE")

        evcstats = db.query(EvCoStatement).from_statement(text("SELECT DISTINCT u_evcostatements.id, u_evcostatements.classn, u_evcostatements.modulel, u_evcostatements.extran, u_evcostatements.processn, u_evcostatements.statementtype "
						+ "FROM u_evco2stat,u_evcostatements "
						+ "WHERE u_evco2stat.id_evcoid=:evc "
                        + "AND u_evco2stat.id_stat=u_evcostatements.ID ")).params(evc=evc).all()

        return evcstats 
    
    def getEvCoToStat(self,evc=-2,db=None):

        if (db == None or evc == -2):
                print ("PARAMETERS EXCEPTION HERE")

        evcotostats = db.query(EvCoToStat).from_statement(text("SELECT DISTINCT u_evco2stat.id, u_evco2stat.id_stat ,u_evco2stat.statementrank "
						+ "FROM u_evco2stat "
						+ "WHERE u_evco2stat.id_evcoid=:evc ")).params(evc=evc).all()

        return evcotostats 
    
    
    def getESMTemplates(self,id_rel=-2,db=None):

        if (db == None or id_rel == -2):
                print ("PARAMETERS EXCEPTION HERE")

        esModTemp = db.query(ESModTemplate).from_statement(text("select U_ESMTEMPLATES.id, U_ESMTEMPLATES.name "
						+ "FROM U_ESMTEMPLATES, u_esmt2rele "
						+ "WHERE u_esmt2rele.id_release=:id_rel "
						+ "and U_ESMTEMPLATES.id = u_esmt2rele.id_esmtemplate")).params(id_rel=id_rel).all()

        return esModTemp
    
    def getConfESModules(self,id_ver=-2,db=None):

        if (db == None or id_ver == -2):
                print ("PARAMETERS EXCEPTION HERE")

        esmodules = db.query(ESModule).from_statement(text(" SELECT u_esmodules.id, u_esmodules.id_template, u_esmodules.name "
						+ "FROM u_esmodules,u_conf2esm "
						+ "WHERE u_conf2esm.id_esmodule=u_esmodules.id "
						+ "and u_conf2esm.id_confver =:ver  ")).params(ver = id_ver).all()

        return esmodules
    
    def getESMTemplateByEsm(self,id_esm=-2,db=None):

        if (db == None or id_esm == -2):
                print ("PARAMETERS EXCEPTION HERE")

        esModTemp = db.query(ESModTemplate).from_statement(text("select U_ESMTEMPLATES.id, U_ESMTEMPLATES.name "
						+ "FROM U_ESMTEMPLATES, u_esmodules "
						+ "WHERE u_esmodules.id_template=U_ESMTEMPLATES.id "
                        + "AND u_esmodules.id=:id_esm")).params(id_esm=id_esm).first()

        return esModTemp
    
    
    def getConfToESMRel(self,id_ver=-2,db=None):

        if (db == None or id_ver == -2):
                print ("PARAMETERS EXCEPTION HERE")

        esmodules = db.query(ConfToEsm).from_statement(text(" SELECT u_conf2esm.id, u_conf2esm.id_esmodule, u_conf2esm.ord "
						+ "FROM u_conf2esm "
						+ "WHERE u_conf2esm.id_confver =:ver ")).params(ver = id_ver).all()

        return esmodules
    
    def getESMTemplateParams(self,id_templ=-2, db=None):
        
        if (id_templ == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        esmtempelements = db.query(ESMTempElement).filter(ESMTempElement.id_esmtemplate==id_templ).all()  
        
        return esmtempelements
    
    def getESModParams(self,id_esm=-2, db=None):
        
        if (id_esm == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        esmtempelements = db.query(ESMElement).filter(ESMElement.id_esmodule==id_esm).all()  
        
        return esmtempelements
    
    
    def getConfSequences(self, id_version=-2, db=None):
        
        elements = []
        if (id_version == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        elements = db.query(Pathelement).from_statement(text("SELECT "
                        + "u_paelements.id, "
                        + "u_paelements.name, "
                        + "u_paelements.paetype "                                       
                        + "FROM u_pathid2pae, u_paelements, u_pathid2conf "
                        + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid " 
#                        + "and u_pathid2pae.id_pathid=:node "
                        + "and u_pathid2pae.id_pae=u_paelements.id "
                        + "and ((u_pathid2pae.lvl=0 and u_paelements.paetype=2) or u_pathid2pae.lvl>0) "
                        + "and u_pathid2conf.id_confver=:leng "
                        + "order by u_pathid2pae.id ")).params(leng=id_version).all()
        
        return elements
    
    #Returns the Sequences Pathitems records (Sequences and their Modules) in the whole ConfVersion
    #@params: 
    #         id_version: id of Confversion table in the confDB
    #         db: database session object
    #
    
    def getConfSequencesItems(self, id_version=-2, db=None):
        
        items = []
        if (id_version == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        items = db.query(Pathitems).from_statement(text("SELECT "
                        + "u_pathid2pae.id, "
                        + "u_pathid2pae.id_pathid, "                                      
                        + "u_pathid2pae.id_pae, "                                       
                        + "u_pathid2pae.id_parent,"
                        + "u_pathid2pae.lvl, " 
                        + "u_pathid2pae.ord "                                            
                        + "FROM u_pathid2pae,u_paelements, u_pathid2conf  "
                        + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid " 
#                        + "and u_pathid2pae.id_pathid=:node "
                        + "and u_pathid2pae.id_pae=u_paelements.id "
                        + "and ((u_pathid2pae.lvl=0 and u_paelements.paetype=2) or u_pathid2pae.lvl>0) "
                        + "and u_pathid2conf.id_confver=:leng "
                        + "order by u_pathid2pae.id ")).params(leng=id_version).all()
        
        return items
    
    def getOUMElements(self,oumId=None, db=None):

        if (oumId==None or db == None):
                print ("PARAMETERS EXCEPTION HERE")

        elements = db.query(OumElement).filter(OumElement.id_streamid == oumId).order_by(OumElement.id).all()  

        return elements
    
    def getConfGPsets(self,id_ver=-2,db=None):

        if (db == None or id_ver == -2):
                print ("PARAMETERS EXCEPTION HERE")

        elements = db.query(Globalpset).from_statement(text("SELECT UNIQUE u_globalpsets.id, u_globalpsets.name, u_globalpsets.tracked, u_conf2gpset.ord "
						+ "FROM u_globalpsets, u_conf2gpset "
						+ "WHERE u_conf2gpset.id_gpset = u_globalpsets.id "
						+ "AND u_conf2gpset.id_confver=:ver order by u_conf2gpset.ord")).params(ver = id_ver).all()

        return elements
    
    def getGpsetElements(self,gpsId=None, db=None):

        if (gpsId==None or db == None):
                print ("PARAMETERS EXCEPTION HERE")

        elements = db.query(GpsetElement).filter(GpsetElement.id_gpset == gpsId).order_by(GpsetElement.id).all()  

        return elements
    
    
    def getConfEDSource(self,id_ver=-2,db=None):

        if (db == None or id_ver == -2):
                print ("PARAMETERS EXCEPTION HERE")

        eds = db.query(EDSource).from_statement(text(" SELECT u_edsources.id, u_edsources.id_template "
						+ "FROM u_edsources,u_conf2eds "
						+ "WHERE u_conf2eds.id_edsource=u_edsources.id "
						+ "and u_conf2eds.id_confver =:ver  ")).params(ver = id_ver).all()
        return eds
    
    def getEDSTemplates(self,id_rel=-2,db=None):

        if (db == None or id_rel == -2):
                print ("PARAMETERS EXCEPTION HERE")

        edsTemp = db.query(EDSourceTemplate).from_statement(text("select u_edstemplates.id, u_edstemplates.name "
						+ "FROM u_edstemplates, u_edst2rele "
						+ "WHERE u_edst2rele.id_release=:id_rel "
						+ "and u_edstemplates.id = u_edst2rele.id_edstemplate")).params(id_rel=id_rel).all()

        return edsTemp
    
    def getConfToEDSRel(self,id_ver=-2,db=None):

        if (db == None or id_ver == -2):
                print ("PARAMETERS EXCEPTION HERE")

        esmodules = db.query(ConfToEds).from_statement(text(" SELECT u_conf2eds.id, u_conf2eds.id_edsource, u_conf2eds.ord "
						+ "FROM u_conf2eds "
						+ "WHERE u_conf2eds.id_confver =:ver ")).params(ver = id_ver).all()

        return esmodules
    
    def getEDSTemplateByEds(self,id_eds=-2,db=None):

        if (db == None or id_eds == -2):
                print ("PARAMETERS EXCEPTION HERE")

        edSrcTemp = db.query(EDSourceTemplate).from_statement(text("select u_edstemplates.id, u_edstemplates.name "
						+ "FROM u_edstemplates, u_edsources "
						+ "WHERE u_edsources.id_template=u_edstemplates.id "
                        + "AND u_edsources.id=:id_eds")).params(id_eds=id_eds).first()

        return edSrcTemp
    
    def getEDSTemplateParams(self,id_templ=-2, db=None):
        
        if (id_templ == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        edstempelements = db.query(EDSTempElement).filter(EDSTempElement.id_edstemplate==id_templ).all()  
        
        return edstempelements
    def getEDSourceParams(self,id_eds=-2, db=None):
        
        if (id_eds == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        edstempelements = db.query(EDSElement).filter(EDSElement.id_edsource==id_eds).all()  
        
        return edstempelements 
    
    def getConfESSource(self,id_ver=-2,db=None):

        if (db == None or id_ver == -2):
                print ("PARAMETERS EXCEPTION HERE")

        ess = db.query(ESSource).from_statement(text(" SELECT u_essources.id, u_essources.id_template "
						+ "FROM u_essources,u_conf2ess "
						+ "WHERE u_conf2ess.id_essource=u_essources.id "
						+ "and u_conf2ess.id_confver =:ver  ")).params(ver = id_ver).all()
        return ess
    
    def getESSTemplates(self,id_rel=-2,db=None):

        if (db == None or id_rel == -2):
                print ("PARAMETERS EXCEPTION HERE")

        essTemp = db.query(ESSourceTemplate).from_statement(text("select u_esstemplates.id, u_esstemplates.name "
						+ "FROM u_esstemplates, u_esst2rele "
						+ "WHERE u_esst2rele.id_release=:id_rel "
						+ "and u_esstemplates.id = u_esst2rele.id_esstemplate")).params(id_rel=id_rel).all()

        return essTemp
    
    def getConfToESSRel(self,id_ver=-2,db=None):

        if (db == None or id_ver == -2):
                print ("PARAMETERS EXCEPTION HERE")

        essources = db.query(ConfToEss).from_statement(text(" SELECT u_conf2ess.id, u_conf2ess.id_essource, u_conf2ess.ord "
						+ "FROM u_conf2ess "
						+ "WHERE u_conf2ess.id_confver =:ver ")).params(ver = id_ver).all()

        return essources
    
    def getESSTemplateByEss(self,id_ess=-2,db=None):

        if (db == None or id_ess == -2):
                print ("PARAMETERS EXCEPTION HERE")

        esSrcTemp = db.query(ESSourceTemplate).from_statement(text("select u_esstemplates.id, u_esstemplates.name "
						+ "FROM u_esstemplates, u_essources "
						+ "WHERE u_essources.id_template=u_esstemplates.id "
                        + "AND u_essources.id=:id_ess")).params(id_ess=id_ess).first()

        return esSrcTemp
    
    def getESSTemplateParams(self,id_templ=-2, db=None):
        
        if (id_templ == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        esstempelements = db.query(ESSTempElement).filter(ESSTempElement.id_esstemplate==id_templ).all()  
        
        return esstempelements
    
    def getESSourceParams(self,id_eds=-2, db=None):
        
        if (id_eds == -2 or db == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        esstempelements = db.query(ESSElement).filter(ESSElement.id_essource==id_eds).all()  
        
        return esstempelements 
    
    