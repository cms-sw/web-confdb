# File confdb_v2/queries.py Description:
# This files contains the implementations of the methods providing the query
# to retrieve records from the ConfDb
#
# Class: ConfDbQueries
from collections import OrderedDict

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.sql import select
from sqlalchemy.sql import text
from sqlalchemy import Sequence
from operator import attrgetter
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

from .tables import *


class ConfDbQueries(object):

    def getPathElements(self, id_pathid, id_version, db, log):
        if (id_pathid == -2 or id_version == -2 or db == None):
            log.error('ERROR: getPathElements - input parameters error')

        query = db.query(Pathelement).from_statement(text("SELECT "
                                                          + "u_paelements.id, "
                                                          + "u_paelements.name, "
                                                          + "u_paelements.paetype "
                                                          + "FROM u_pathid2pae, u_paelements, u_pathid2conf "
                                                          + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid "
                                                          + "and u_pathid2pae.id_pathid=:node "
                                                          + "and u_pathid2pae.id_pae=u_paelements.id "
                                                          + "and u_pathid2conf.id_confver=:leng "
                                                          + "order by u_pathid2pae.id ")).params(node=id_pathid,
                                                                                                 leng=id_version)
        results = query.all()
        return results

    def getPathItems(self, id_pathid, id_version, db, log):
        if (id_pathid == -2 or id_version == -2 or db == None):
            log.error('ERROR: getPathItems - input parameters error')

        query = db.query(Pathitems).from_statement(text("SELECT "
                                                        + "u_pathid2pae.id, "
                                                        + "u_pathid2pae.id_pathid, "
                                                        + "u_pathid2pae.id_pae, "
                                                        + "u_pathid2pae.id_parent,"
                                                        + "u_pathid2pae.lvl, "
                                                        + "u_pathid2pae.ord, "
                                                        + "u_pathid2pae.operator "
                                                        + "FROM u_pathid2pae, u_paelements, u_pathid2conf  "
                                                        + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid "
                                                        + "and u_pathid2pae.id_pathid=:node "
                                                        + "and u_pathid2pae.id_pae=u_paelements.id "
                                                        + "and u_pathid2conf.id_confver=:leng "
                                                        + "order by u_pathid2pae.id ")).params(node=id_pathid,
                                                                                               leng=id_version)
        results = query.all()
        return results

    @staticmethod
    def get_conf_pathitems(id_version, db, log):
        if id_version == -2 or db is None:
            log.error('ERROR: getConfPathItems - input parameters error')

        query = db.query(Pathitems).from_statement(text("SELECT "
                                                        + "u_pathid2pae.id, "
                                                        + "u_pathid2pae.id_pathid, "
                                                        + "u_pathid2pae.id_pae, "
                                                        + "u_pathid2pae.id_parent,"
                                                        + "u_pathid2pae.lvl, "
                                                        + "u_pathid2pae.ord, "
                                                        + "u_pathid2pae.operator "
                                                        + "FROM u_pathid2pae, u_paelements, u_pathid2conf  "
                                                        + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid "
                                                        + "and u_pathid2pae.id_pae=u_paelements.id "
                                                        + "and u_pathid2conf.id_confver=:ver "
                                                        + "order by u_pathid2pae.id ")).params(ver=id_version)

        results = query.all()
        return results

    # Returns the Sequences Paelements records (Sequences and their Modules) in a given path
    # @params:
    #         id_version: id of Confversion table in the confDB
    #         id_pathid: id of path_id table in the confDB
    #         db: database session object
    #
    def getCompletePathSequences(self, id_pathid, id_version, db, log):

        elements = []
        if (id_pathid == -2 or id_version == -2 or db == None):
            log.error('ERROR: getCompletePathSequences - input parameters error')

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
                                                             + "order by u_pathid2pae.id ")).params(node=id_pathid,
                                                                                                    leng=id_version).all()

        return elements

    # Returns the Sequences Pathitems records (Sequences and their Modules) in a given path
    # @params:
    #         id_version: id of Confversion table in the confDB
    #         id_pathid: id of path_id table in the confDB
    #         db: database session object
    #
    def getCompletePathSequencesItems(self, id_pathid, id_version, db, log):

        items = []
        if (id_pathid == -2 or id_version == -2 or db == None):
            log.error('ERROR: getCompletePathSequencesItems - input parameters error')

        items = db.query(Pathitems).from_statement(text("SELECT "
                                                        + "u_pathid2pae.id, "
                                                        + "u_pathid2pae.id_pathid, "
                                                        + "u_pathid2pae.id_pae, "
                                                        + "u_pathid2pae.id_parent,"
                                                        + "u_pathid2pae.lvl, "
                                                        + "u_pathid2pae.ord, "
                                                        + "u_pathid2pae.operator "
                                                        + "FROM u_pathid2pae, u_paelements, u_pathid2conf  "
                                                        + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid "
                                                        + "and u_pathid2pae.id_pathid=:node "
                                                        + "and u_pathid2pae.id_pae=u_paelements.id "
                                                        + "and ((u_pathid2pae.lvl=0 and u_paelements.paetype=2) or u_pathid2pae.lvl>0) "
                                                        + "and u_pathid2conf.id_confver=:leng "
                                                        + "order by u_pathid2pae.id ")).params(node=id_pathid,
                                                                                               leng=id_version).all()

        return items

    # Returns the Streamid associated with the output module present in a given End Path
    # @params:
    #
    #         id_pathid: id of path_id table in the confDB
    #         db: database session object
    #
    def getOumStreamid(self, id_pathid, db, log):

        if (id_pathid == -2 or db == None):
            log.error('ERROR: getOumStreamid - input parameters error')

        oum = db.query(PathidToOutM).from_statement(text("SELECT DISTINCT "
                                                         + "u_pathid2outm.id, "
                                                         + "u_pathid2outm.id_pathid, "
                                                         + "u_pathid2outm.id_streamid, "
                                                         + "u_pathid2outm.ord "
                                                         + "FROM u_pathid2outm "
                                                         + "WHERE u_pathid2outm.id_pathid=:node ")).params(
            node=id_pathid).first()

        return oum

    # Returns the Stream from the streamid for an End Path
    # @params:
    #
    #         id_pathid: id of path_id table in the confDB
    #         db: database session object
    #
    def getStreamid(self, id_streamid, db, log):

        if (id_streamid == -2 or db == None):
            log.error('ERROR: getStreamid - input parameters error')

        stid = db.query(StreamId).from_statement(text("SELECT DISTINCT "
                                                      + "u_streamids.id, u_streamids.id_stream "
                                                      + "FROM u_streamids "
                                                      + "WHERE u_streamids.id=:node ")).params(node=id_streamid).first()

        return stid

    # Returns the Pathitems records (Modules) present in the level 0 of a given Path
    # @params:
    #         id_version: id of Confversion table in the confDB
    #         id_pathid: id of path_id table in the confDB
    #         db: database session object
    #
    def getLevelZeroPathItems(self, id_pathid, id_version, db, log):

        items = []
        if (id_pathid == -2 or id_version == -2 or db == None):
            log.error('ERROR: getLevelZeroPathItems - input parameters error')

        items = db.query(Pathitems).from_statement(text("SELECT "
                                                        + "u_pathid2pae.id, "
                                                        + "u_pathid2pae.id_pathid, "
                                                        + "u_pathid2pae.id_pae, "
                                                        + "u_pathid2pae.id_parent,"
                                                        + "u_pathid2pae.lvl, "
                                                        + "u_pathid2pae.ord, "
                                                        + "u_pathid2pae.operator "
                                                        + "FROM u_pathid2pae, u_paelements, u_pathid2conf  "
                                                        + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid "
                                                        + "and u_pathid2pae.id_pathid=:node "
                                                        + "and u_pathid2pae.id_pae=u_paelements.id "
                                                        + "and (u_pathid2pae.lvl=0 and u_paelements.paetype!=2) "
                                                        + "and u_pathid2conf.id_confver=:leng "
                                                        + "order by u_pathid2pae.id ")).params(node=id_pathid,
                                                                                               leng=id_version).all()

        return items

    # Returns the level zero Paelements records (Modules) in a given path
    # @params:
    #         id_version: id of Confversion table in the confDB
    #         id_pathid: id of path_id table in the confDB
    #         db: database session object
    #
    def getLevelZeroPaelements(self, id_pathid, id_version, db, log):

        elements = []
        if (id_pathid == -2 or id_version == -2 or db == None):
            log.error('ERROR: getLevelZeroPaelements - input parameters error')

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
                                                             + "order by u_pathid2pae.id ")).params(node=id_pathid,
                                                                                                    leng=id_version).all()

        return elements

    # Returns the Version from the id
    # @params:
    #         id_ver: id of ConfVersion table in the confDB
    #         db: database session object
    #
    def getVersion(self, id_ver, db, log):

        if (id_ver == -2 or db == None):
            log.error('ERROR: getVersion - input parameters error')

        version = db.query(Version).get(id_ver)

        return version

    # Returns the paths of a given ConfVersion
    # @params:
    #         id_version: id of ConfVersion table in the confDB
    #         db: database session object
    #
    def getPaths(self, id_version, db, log):

        pats = []
        if (id_version == -2 or db == None):
            log.error('ERROR: getPaths - input parameters error')

        pats = db.query(Pathids).from_statement(text("SELECT u_pathids.id, u_pathids.id_path, u_pathids.isendpath "
                                                     + "FROM  u_pathids, u_pathid2conf "
                                                     + "WHERE u_pathids.id = u_pathid2conf.id_pathid "
                                                     + "AND u_pathid2conf.id_confver=:idv AND u_pathids.isEndPath = 0 order by u_pathid2conf.ord")).params(
            idv=id_version).all()

        return pats

    # Returns the END paths of a given ConfVersion
    # @params:
    #         id_version: id of ConfVersion table in the confDB
    #         db: database session object
    #
    def getEndPaths(self, id_version, db, log):

        pats = []
        if (id_version == -2 or db == None):
            log.error('ERROR: getEndPaths - input parameters error')

        pats = db.query(Pathids).from_statement(text("SELECT u_pathids.id, u_pathids.id_path, u_pathids.isendpath "
                                                     + "FROM  u_pathids, u_pathid2conf "
                                                     + "WHERE u_pathids.id = u_pathid2conf.id_pathid "
                                                     + "AND u_pathid2conf.id_confver=:idv AND u_pathids.isEndPath = 1 order by u_pathid2conf.ord")).params(
            idv=id_version).all()

        return pats


    def getPathName(self, id_pathid, id_ver, db, log):

        if (id_pathid == -2 or db == None or id_ver == -2):
            log.error('ERROR: getPathName - input parameters error')

        patname = db.query(Paths).from_statement(text("SELECT u_paths.id, u_paths.name "
                                                      + "FROM  u_pathids, u_pathid2conf, u_paths "
                                                      + "WHERE u_pathids.id = u_pathid2conf.id_pathid "
                                                      + "AND u_pathids.id_path = u_paths.id "
                                                      + "AND u_pathids.id=:id_pid "
                                                      + "AND u_pathid2conf.id_confver=:idv ")).params(idv=id_ver,
                                                                                                      id_pid=id_pathid).first()

        return patname

    def getPathContact(self, id_pathid, id_ver, db, log):

        if (id_pathid == -2 or db == None or id_ver == -2):
            log.error('ERROR: getPathName - input parameters error')

        #
        contact = db.query(Pathids).filter(Pathids.id == id_pathid).first()

        return contact

    def getPathDescription(self, id_pathid, id_ver, db, log):

        if (id_pathid == -2 or db == None or id_ver == -2):
            log.error('ERROR: getPathName - input parameters error')

        description = db.query(Pathids).filter(Pathids.id == id_pathid).first()

        return description

    # Returns the template from the module (Paelement) id
    # @params:
    #         id_pae: id of Paelement table in the confDB
    #         db: database session object
    #
    def getTemplateFromPae(self, id_pae, db, log):

        if (id_pae == -2 or db == None):
            log.error('ERROR: getTemplateFromPae - input parameters error')

        template_id = db.query(ModToTemp).filter(ModToTemp.id_pae == id_pae).first()
        template = db.query(ModTemplate).filter(ModTemplate.id == template_id.id_templ).first()

        return template

    def getTemplateParams(self, id_templ, db, log):

        if (id_templ == -2 or db == None):
            log.error('ERROR: getTemplateParams - input parameters error')

        tempelements = db.query(ModTelement).filter(ModTelement.id_modtemp == id_templ).order_by(ModTelement.id).all()

        return tempelements

    def getModuleParamItems(self, id_pae, db, log):

        if (id_pae == -2 or db == None):
            log.error('ERROR: getModuleParamItems - input parameters error')

        q = db.query(Moduleitem).from_statement(text("SELECT DISTINCT u_pae2moe.id, u_pae2moe.id_pae, u_pae2moe.id_moe, u_pae2moe.lvl, u_pae2moe.ord "
        + "FROM u_pae2moe INNER JOIN ("
        + " SELECT MAX(u_pae2moe.id) maxid, u_pae2moe.id_pae, u_pae2moe.id_moe "
        + " FROM u_pae2moe WHERE u_pae2moe.id_pae =:id_pae GROUP BY u_pae2moe.id_moe, u_pae2moe.id_pae ORDER BY u_pae2moe.id_moe) myPae2Moe "
        + "ON u_pae2moe.id = myPae2Moe.maxid ORDER BY u_pae2moe.id_moe")).params(id_pae=id_pae)

        items = q.all()

        return items



    def get_mod2param_by_ver(self, id_ver, db, log):

        if (db == None or id_ver == None):
            log.error('ERROR: getMod2TempByVer - input parameters error')

        mod2temps = db.query(Moduleitem).from_statement(
            text("SELECT UNIQUE u_pae2moe.id, u_pae2moe.id_pae, u_pae2moe.id_moe, u_pae2moe.lvl, u_pae2moe.ord "
                 + "FROM u_pathid2pae, u_paelements, u_pathid2conf, u_pae2moe "
                 + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid "
                 + "and u_pathid2pae.id_pae=u_paelements.id "
                 + "and u_paelements.paetype=1 "
                 + "and u_pae2moe.id_pae=u_paelements.id "
                 + "and u_pathid2conf.id_confver=:ver")).params(ver=id_ver).all()

        return mod2temps


    def getModuleParamItemsOne(self, id_pae, db, log):

        if (id_pae == -2 or db == None):
            log.error('ERROR: getModuleParamItems - input parameters error')

        query = db.query(ModuleitemFull).from_statement(text("""SELECT
                u_pae2moe.id id,
                u_pae2moe.id_pae id_pae,
                u_pae2moe.id_moe id_moe,
                u_pae2moe.lvl lvl,
                u_pae2moe.ord ord,
                u_moelements.name name,
                u_moelements.moetype moetype,
                u_moelements.paramtype paramtype,
                u_moelements.tracked tracked,
                u_moelements.hex hex,
                u_moelements.value value,
                u_moelements.valuelob valuelob
            FROM
                u_pae2moe,
                u_moelements,
                (SELECT MAX(u_pae2moe.id) id FROM u_pae2moe WHERE u_pae2moe.id_pae = :id_pae GROUP BY u_pae2moe.id_moe, u_pae2moe.id_pae) unique_id
            WHERE
                u_pae2moe.id = unique_id.id AND
                u_moelements.id = u_pae2moe.id_moe
            ORDER BY u_pae2moe.id_moe""")).params(id_pae=id_pae)

        elements = query.all()
        return elements


    def getModuleParamElements(self, moeIds, db, log):

        if (moeIds==None or db == None):
                log.error('ERROR: getModuleParamElements - input parameters error')

        elements = db.query(Modelement).filter(Modelement.id.in_(moeIds)).order_by(Modelement.id).all()

        return elements


    def getAllDirectories(self, db, log):

        if (db == None):
                log.error('ERROR: getAllDirectories - input parameters error')

        directories = db.query(Directory).all()

        return directories

    def getDirectoryByName(self, name, db, log):

        if (db == None or name==""):
                log.error('ERROR: getDirectoryByName - input parameters error')

        directory = db.query(Directory).filter(Directory.name == name).first()

        return directory

    def getChildDirectories(self, dir_id, db, log):

        if (db == None or dir_id == -2):
            log.error('ERROR: getDirectoryByName - input parameters error')

        directories = db.query(Directory).filter(Directory.id_parentdir == dir_id).all()

        return directories

    def getConfigsInDir(self, id_parent, db, log):

        if (db == None or id_parent == -2):
            log.error('ERROR: getConfigsInDir - input parameters error')

        configs = db.query(Configuration).from_statement(text(
            "SELECT  u_configurations.id, u_configurations.name FROM u_configurations, u_confversions WHERE u_configurations.id = u_confversions.id_config and u_confversions.id_parentdir=:id_par")).params(
            id_par=id_parent).all()

        return configs

    def getConfVersions(self, id_config, db, log):

        if (db == None or id_config == -2):
            log.error('ERROR: getConfVersions - input parameters error')

        versions = db.query(Version).filter(Version.id_config == id_config).all()

        return versions

    def getModToTempByPae(self, id_pae, db, log):

        if (db == None or id_pae == -2):
            log.error('ERROR: getModToTempByPae - input parameters error')

        mod2temp = db.query(ModToTemp).filter(ModToTemp.id_pae == id_pae).first()

        return mod2temp

    def getMod2TempByPaelemets(self, id_paes, db, log):

        if (db == None or id_paes == None):
            log.error('ERROR: getMod2TempByPaelemets - input parameters error')

        mod2temps = db.query(ModToTemp).filter(ModToTemp.id_pae.in_(id_paes)).all()

        return mod2temps

    def getMod2TempByVer(self, id_ver, db, log):

        if (db == None or id_ver == None):
            log.error('ERROR: getMod2TempByVer - input parameters error')

        mod2temps = db.query(ModToTemp).from_statement(
            text("SELECT UNIQUE u_mod2templ.id, u_mod2templ.id_pae, u_mod2templ.id_templ "
                 + "FROM u_pathid2pae, u_paelements, u_pathid2conf, u_mod2templ "
                 + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid "
                 + "and u_pathid2pae.id_pae=u_paelements.id "
                 + "and u_paelements.paetype=1 "
                 + "and u_mod2templ.id_pae=u_paelements.id "
                 + "and u_pathid2conf.id_confver=:ver")).params(ver=id_ver).all()

        return mod2temps

    def getTempIdByPae(self, id_pae, db, log):

        if (db == None or id_pae == -2):
            log.error('ERROR: getTempIdByPae - input parameters error')

        mod2temps = db.query(ModToTemp.id_templ).filter(ModToTemp.id_pae == id_pae).first()

        return mod2temps[0]

    def getModTemplate(self, id_temp, db, log):

        if (db == None or id_temp == -2):
            log.error('ERROR: getModTemplate - input parameters error')

        modTemp = db.query(ModTemplate).filter(ModTemplate.id == id_temp).first()

        return modTemp

    def getPaelement(self, id_pae, db, log):

        if (db == None or id_pae == -2):
            log.error('ERROR: getPaelement - input parameters error')

        element = db.query(Pathelement).get(id_pae)

        return element

    def getConfModules(self, id_ver, db, log):

        if (db == None or id_ver == -2):
            log.error('ERROR: getConfModules - input parameters error')

        elements = db.query(Pathelement).from_statement(text("SELECT UNIQUE u_paelements.id, u_paelements.name "
                                                             + "FROM u_pathid2pae, u_paelements, u_pathid2conf "  # , u_mod2templ
                                                             + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid "
                                                             + "and u_pathid2pae.id_pae=u_paelements.id "
                                                             + "and u_paelements.paetype=1 "
                                                             #                       + "and u_mod2templ.id_pae=u_paelements.id "
                                                             + "and u_pathid2conf.id_confver=:ver order by u_paelements.name")).params(
            ver=id_ver).all()

        return elements

    @staticmethod
    def get_conf_paelements(id_ver, db, log):
        if db is None or id_ver == -2:
            log.error('ERROR: getConfModules - input parameters error')
        elements = db.query(Pathelement).from_statement(text("SELECT UNIQUE u_paelements.id, u_paelements.name, u_paelements.paetype "
                                                             + "FROM u_pathid2pae, u_paelements, u_pathid2conf "
                                                             + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid "
                                                             + "and u_pathid2pae.id_pae=u_paelements.id "
                                                             + "and u_pathid2conf.id_confver=:ver order by u_paelements.name")
                                                        ).params(ver=id_ver).all()
        return elements

    def getRelTemplates(self, id_rel, db, log):

        if (db == None or id_rel == -2):
            log.error('ERROR: getRelTemplates - input parameters error')

        templates = db.query(ModTemplate).from_statement(text("select u_moduletemplates.id, u_moduletemplates.name, "
                                                              + " u_moduletemplates.id_mtype "
                                                              + "from u_moduletemplates, u_modt2rele "
                                                              + "where u_modt2rele.id_release=:id_rel "
                                                              + "and u_modt2rele.id_modtemplate=u_moduletemplates.id ")).params(
            id_rel=id_rel).all()

        return templates

    def getAPathidByPae(self, id_rel, db, log):

        if (db == None or id_rel == -2):
            log.error('ERROR: getAPathidByPae - input parameters error')

        templates = db.query(ModTemplate).from_statement(text("select u_moduletemplates.id, u_moduletemplates.name, "
                                                              + " u_moduletemplates.id_mtype "
                                                              + "from u_moduletemplates, u_modt2rele "
                                                              + "where u_modt2rele.id_release=:id_rel "
                                                              + "and u_modt2rele.id_modtemplate=u_moduletemplates.id ")).params(
            id_rel=id_rel).all()

        return templates

    def getConfServices(self, id_ver, db, log):

        if (db == None or id_ver == -2):
            log.error('ERROR: getConfServices - input parameters error')

        elements = db.query(Service).from_statement(
            text("SELECT UNIQUE u_services.id, u_services.id_template, u_conf2srv.ord "
                 + "FROM u_services, u_conf2srv "
                 + "WHERE u_conf2srv.id_service = u_services.id "
                 + "AND u_conf2srv.id_confver=:ver order by u_conf2srv.ord")).params(ver=id_ver).all()

        return elements

    def getConfPrescale(self, id_ver, id_templ, db, log):

        if (db == None or id_ver == -2 or id_templ == -2):
            log.error('ERROR: getConfPrescale - input parameters error')

        elements = db.query(Service).from_statement(
            text("SELECT UNIQUE u_services.id, u_services.id_template, u_conf2srv.ord "
                 + "FROM u_services, u_conf2srv "
                 + "WHERE u_conf2srv.id_service = u_services.id "
                 + "AND u_services.id_template=:id_templ "
                 + "AND u_conf2srv.id_confver=:ver order by u_conf2srv.ord")).params(ver=id_ver,
                                                                                     id_templ=id_templ).first()

        return elements

    def getConfPrescaleTemplate(self, id_rel, db, log):

        if (db == None or id_rel == -2):
            log.error('ERROR: getConfPrescaleTemplate - input parameters error')

        prescaleTemplate = db.query(SrvTemplate).from_statement(text("SELECT u_srvtemplates.id, u_srvtemplates.name "
                                                                     + "FROM u_srvtemplates, u_srvt2rele "
                                                                     + "WHERE u_srvt2rele.id_release=:id_rel "
                                                                     + "AND u_srvtemplates.name=:name "
                                                                     + "AND u_srvt2rele.id_srvtemplate=u_srvtemplates.id ")).params(
            id_rel=id_rel, name="PrescaleService").first()

        return prescaleTemplate

    def getRelSrvTemplates(self, id_rel, db, log):

        if (db == None or id_rel == -2):
            log.error('ERROR: getRelSrvTemplates - input parameters error')

        templates = db.query(SrvTemplate).from_statement(text("SELECT u_srvtemplates.id, u_srvtemplates.name "
                                                              + "FROM u_srvtemplates, u_srvt2rele "
                                                              + "WHERE u_srvt2rele.id_release=:id_rel "
                                                              + "AND u_srvt2rele.id_srvtemplate=u_srvtemplates.id ")).params(
            id_rel=id_rel).all()

        return templates

    def getSrvTemplateBySrv(self, sid, db, log):

        if (db == None or sid == -2):
            log.error('ERROR: getSrvTemplateBySrv - input parameters error')

        template = db.query(SrvTemplate).from_statement(text("SELECT u_srvtemplates.id, u_srvtemplates.name "
                                                             + "FROM u_srvtemplates, u_services "
                                                             + "WHERE u_services.id_template=u_srvtemplates.id "
                                                             + "AND u_services.id=:sid")).params(sid=sid).first()

        return template

    def getSrvTemplateParams(self, id_templ, db, log):

        if (id_templ == -2 or db == None):
            log.error('ERROR: getSrvTemplateParams - input parameters error')

        tempelements = db.query(SrvTempElement).filter(SrvTempElement.id_srvtemplate == id_templ).order_by(
            SrvTempElement.id).all()

        return tempelements

    def getServiceParamElements(self, srvId, db, log):

        if (srvId == None or db == None):
            log.error('ERROR: getServiceParamElements - input parameters error')

        elements = db.query(SrvElement).filter(SrvElement.id_service == srvId).order_by(SrvElement.id).all()

        return elements

    def getConfStreams(self, ver, db, log):

        if (db == None or ver == -2):
            log.error('ERROR: getConfStreams - input parameters error')

        streams = db.query(StreamId).from_statement(text("SELECT DISTINCT u_streamids.id, u_streamids.id_stream "
                                                         + "FROM u_conf2strdst, u_streamids "
                                                         + "WHERE u_streamids.id=u_conf2strdst.id_streamid "
                                                         + "and u_conf2strdst.id_confver=:ver ")).params(ver=ver).all()

        return streams

    def getConfDatasets(self, ver, db, log):

        if (db == None or ver == -2):
            log.error('ERROR: getConfDatasets - input parameters error')

        datasets = db.query(DatasetId).from_statement(text("SELECT DISTINCT u_datasetids.id, u_datasetids.id_dataset "
                                                           + "FROM u_conf2strdst, u_datasetids "
                                                           + "WHERE u_datasetids.id=u_conf2strdst.id_datasetid "
                                                           + "and u_conf2strdst.id_confver=:ver ")).params(
            ver=ver).all()

        return datasets

    def getConfStrDatRels(self, ver, db, log):
        if (db == None or ver == -2):
            log.error('ERROR: getConfStrDatRels - input parameters error')

        rels = db.query(ConfToStrDat).from_statement(text(
            "SELECT DISTINCT u_conf2strdst.id, u_conf2strdst.id_confver, u_conf2strdst.id_streamid, u_conf2strdst.id_datasetid "
            + "FROM u_conf2strdst "
            + "WHERE u_conf2strdst.id_confver =:ver ")).params(ver=ver).all()

        return rels

    def getDatasetPathids(self, ver, dstid, db, log):

        if (db == None or ver == -2 or dstid == -2):
            log.error('ERROR: getDatasetPathids - input parameters error')

        pathids = db.query(Pathids).from_statement(text("SELECT distinct u_pathids.id "
                                                        + "FROM u_pathid2strdst, u_conf2strdst, u_pathids "
                                                        + "WHERE u_conf2strdst.id_confver=:ver "
                                                        + "and u_pathids.id = u_pathid2strdst.id_pathid "
                                                        + "and u_conf2strdst.id_datasetid=:dstid "
                                                        + "and u_conf2strdst.id_datasetid=u_pathid2strdst.id_datasetid ")).params(
            ver=ver, dstid=dstid).all()

        return pathids

    def getConfEventContents(self, ver, db, log):

        if (db == None or ver == -2):
            log.error('ERROR: getConfEventContents - input parameters error')

        evcontents = db.query(EventContentId).from_statement(
            text("select U_EVENTCONTENTIDS.id , U_EVENTCONTENTIDS.id_evco "
                 + "from U_EVENTCONTENTIDS, U_CONF2EVCO "
                 + "where U_CONF2EVCO.ID_EVCOID=U_EVENTCONTENTIDS.id "
                 + "and U_CONF2EVCO.id_confver=:ver")).params(ver=ver).all()

        return evcontents

    def getEvCoToStream(self, ver, db, log):

        if (db == None or ver == -2):
            log.error('ERROR: getEvCoToStream - input parameters error')

        relEvCoToStr = db.query(EvCoToStream).from_statement(
            text("SELECT DISTINCT u_EVCO2STREAM.id, u_EVCO2STREAM.id_streamid, u_EVCO2STREAM.id_evcoid "
                 + "FROM u_EVENTCONTENTIDS, u_EVCO2STREAM, u_conf2evco "
                 + "WHERE u_EVCO2STREAM.id_evcoid=u_EVENTCONTENTIDS.ID "
                 + "AND u_conf2evco.id_evcoid=u_EVENTCONTENTIDS.ID "
                 + "AND u_conf2evco.id_confver=:ver ")).params(ver=ver).all()

        return relEvCoToStr

    def getEvCoStatements(self, evc, db, log):

        if (db == None or evc == -2):
            log.error('ERROR: getPathItems - input parameters error')

        evcstats = db.query(EvCoStatement).from_statement(text(
            "SELECT DISTINCT u_evcostatements.id, u_evcostatements.classn, u_evcostatements.modulel, u_evcostatements.extran, u_evcostatements.processn, u_evcostatements.statementtype "
            + "FROM u_evco2stat, u_evcostatements "
            + "WHERE u_evco2stat.id_evcoid=:evc "
            + "AND u_evco2stat.id_stat=u_evcostatements.ID ")).params(evc=evc).all()

        return evcstats

    def getEvCoToStat(self, evc, db, log):

        if (db == None or evc == -2):
            log.error('ERROR: getEvCoToStat - input parameters error')

        evcotostats = db.query(EvCoToStat).from_statement(
            text("SELECT DISTINCT u_evco2stat.id, u_evco2stat.id_stat , u_evco2stat.statementrank "
                 + "FROM u_evco2stat "
                 + "WHERE u_evco2stat.id_evcoid=:evc ")).params(evc=evc).all()

        return evcotostats

    def getESMTemplates(self, id_rel, db, log):

        if (db == None or id_rel == -2):
            log.error('ERROR: getESMTemplates - input parameters error')

        esModTemp = db.query(ESModTemplate).from_statement(text("select U_ESMTEMPLATES.id, U_ESMTEMPLATES.name "
                                                                + "FROM U_ESMTEMPLATES, u_esmt2rele "
                                                                + "WHERE u_esmt2rele.id_release=:id_rel "
                                                                + "and U_ESMTEMPLATES.id = u_esmt2rele.id_esmtemplate")).params(
            id_rel=id_rel).all()

        return esModTemp

    def getConfESModules(self, id_ver, db, log):

        if (db == None or id_ver == -2):
            log.error('ERROR: getConfESModules - input parameters error')

        esmodules = db.query(ESModule).from_statement(
            text(" SELECT u_esmodules.id, u_esmodules.id_template, u_esmodules.name "
                 + "FROM u_esmodules, u_conf2esm "
                 + "WHERE u_conf2esm.id_esmodule=u_esmodules.id "
                 + "and u_conf2esm.id_confver =:ver  ")).params(ver=id_ver).all()

        return esmodules

    def getESMTemplateByEsm(self, id_esm, db, log):

        if (db == None or id_esm == -2):
            log.error('ERROR: getESMTemplateByEsm - input parameters error')

        esModTemp = db.query(ESModTemplate).from_statement(text("select U_ESMTEMPLATES.id, U_ESMTEMPLATES.name "
                                                                + "FROM U_ESMTEMPLATES, u_esmodules "
                                                                + "WHERE u_esmodules.id_template=U_ESMTEMPLATES.id "
                                                                + "AND u_esmodules.id=:id_esm")).params(
            id_esm=id_esm).first()

        return esModTemp

    def getConfToESMRel(self, id_ver, db, log):

        if (db == None or id_ver == -2):
            log.error('ERROR: getConfToESMRel - input parameters error')

        esmodules = db.query(ConfToEsm).from_statement(
            text(" SELECT u_conf2esm.id, u_conf2esm.id_esmodule, u_conf2esm.ord "
                 + "FROM u_conf2esm "
                 + "WHERE u_conf2esm.id_confver =:ver ")).params(ver=id_ver).all()

        return esmodules

    def getESMTemplateParams(self, id_templ, db, log):

        if (id_templ == -2 or db == None):
            log.error('ERROR: getESMTemplateParams - input parameters error')

        esmtempelements = db.query(ESMTempElement).filter(ESMTempElement.id_esmtemplate == id_templ).order_by(
            ESMTempElement.id).all()

        return esmtempelements

    def getESModParams(self, id_esm, db, log):

        if (id_esm == -2 or db == None):
            log.error('ERROR: getESModParams - input parameters error')

        esmtempelements = db.query(ESMElement).filter(ESMElement.id_esmodule == id_esm).order_by(ESMElement.id).all()

        return esmtempelements

    def getConfSequences(self, id_version, db, log):

        elements = []
        if (id_version == -2 or db == None):
            log.error('ERROR: getConfSequences - input parameters error')

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
                                                             + "order by u_pathid2pae.id ")).params(
            leng=id_version).all()

        return elements

    # Returns the Sequences Pathitems records (Sequences and their Modules) in the whole ConfVersion
    # @params:
    #         id_version: id of Confversion table in the confDB
    #         db: database session object
    #

    def getConfSequencesItems(self, id_version, db, log):

        items = []
        if (id_version == -2 or db == None):
            log.error('ERROR: getConfSequencesItems - input parameters error')

        items = db.query(Pathitems).from_statement(text("SELECT "
                                                        + "u_pathid2pae.id, "
                                                        + "u_pathid2pae.id_pathid, "
                                                        + "u_pathid2pae.id_pae, "
                                                        + "u_pathid2pae.id_parent,"
                                                        + "u_pathid2pae.lvl, "
                                                        + "u_pathid2pae.ord "
                                                        + "FROM u_pathid2pae, u_paelements, u_pathid2conf  "
                                                        + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid "
                                                        #                        + "and u_pathid2pae.id_pathid=:node "
                                                        + "and u_pathid2pae.id_pae=u_paelements.id "
                                                        + "and ((u_pathid2pae.lvl=0 and u_paelements.paetype=2) or u_pathid2pae.lvl>0) "
                                                        + "and u_pathid2conf.id_confver=:leng "
                                                        + "order by u_pathid2pae.id ")).params(leng=id_version).all()

        return items

    def getOUMElements(self, oumId, db, log):

        if (oumId == None or db == None):
            log.error('ERROR: getOUMElements - input parameters error')

        elements = db.query(OumElement).from_statement(text("select u_outmelements.* from "
                                                            + "u_outmelements, "
                                                            + "(select max(id) as id from u_outmelements group by name, lvl, id_streamid) unique_id "
                                                            + "where u_outmelements.id_streamid = :streamid "
                                                            + "and u_outmelements.id = unique_id.id "
                                                            + "order by u_outmelements.id ")).params(
            streamid=oumId).all()

        return elements

    def getConfGPsets(self, id_ver, db, log):

        if (db == None or id_ver == -2):
            log.error('ERROR: getConfGPsets - input parameters error')

        elements = db.query(Globalpset).from_statement(
            text("SELECT UNIQUE u_globalpsets.id, u_globalpsets.name, u_globalpsets.tracked, u_conf2gpset.ord "
                 + "FROM u_globalpsets, u_conf2gpset "
                 + "WHERE u_conf2gpset.id_gpset = u_globalpsets.id "
                 + "AND u_conf2gpset.id_confver=:ver order by u_conf2gpset.ord")).params(ver=id_ver).all()

        return elements

    def getGpsetElements(self, gpsId, db, log):

        if (gpsId == None or db == None):
            log.error('ERROR: getGpsetElements - input parameters error')

        elements = db.query(GpsetElement).filter(GpsetElement.id_gpset == gpsId).order_by(GpsetElement.id).all()

        return elements

    def getConfEDSource(self, id_ver, db, log):

        if (db == None or id_ver == -2):
            log.error('ERROR: getConfEDSource - input parameters error')

        eds = db.query(EDSource).from_statement(text(" SELECT u_edsources.id, u_edsources.id_template "
                                                     + "FROM u_edsources, u_conf2eds "
                                                     + "WHERE u_conf2eds.id_edsource=u_edsources.id "
                                                     + "and u_conf2eds.id_confver =:ver  ")).params(ver=id_ver).all()
        return eds

    def getEDSTemplates(self, id_rel, db, log):

        if (db == None or id_rel == -2):
            log.error('ERROR: getEDSTemplates - input parameters error')

        edsTemp = db.query(EDSourceTemplate).from_statement(text("select u_edstemplates.id, u_edstemplates.name "
                                                                 + "FROM u_edstemplates, u_edst2rele "
                                                                 + "WHERE u_edst2rele.id_release=:id_rel "
                                                                 + "and u_edstemplates.id = u_edst2rele.id_edstemplate")).params(
            id_rel=id_rel).all()

        return edsTemp

    def getConfToEDSRel(self, id_ver, db, log):

        if (db == None or id_ver == -2):
            log.error('ERROR: getPathItems - input parameters error')

        esmodules = db.query(ConfToEds).from_statement(
            text(" SELECT u_conf2eds.id, u_conf2eds.id_edsource, u_conf2eds.ord "
                 + "FROM u_conf2eds "
                 + "WHERE u_conf2eds.id_confver =:ver ")).params(ver=id_ver).all()

        return esmodules

    def getEDSTemplateByEds(self, id_eds, db, log):

        if (db == None or id_eds == -2):
            log.error('ERROR: getEDSTemplateByEds - input parameters error')

        edSrcTemp = db.query(EDSourceTemplate).from_statement(text("select u_edstemplates.id, u_edstemplates.name "
                                                                   + "FROM u_edstemplates, u_edsources "
                                                                   + "WHERE u_edsources.id_template=u_edstemplates.id "
                                                                   + "AND u_edsources.id=:id_eds")).params(
            id_eds=id_eds).first()

        return edSrcTemp

    def getEDSTemplateParams(self, id_templ, db, log):

        if (id_templ == -2 or db == None):
            log.error('ERROR: getEDSTemplateParams - input parameters error')

        edstempelements = db.query(EDSTempElement).filter(EDSTempElement.id_edstemplate == id_templ).order_by(
            EDSTempElement.id).all()

        return edstempelements

    def getEDSourceParams(self, id_eds, db, log):

        if (id_eds == -2 or db == None):
            log.error('ERROR: getEDSourceParams - input parameters error')

        edstempelements = db.query(EDSElement).filter(EDSElement.id_edsource == id_eds).order_by(EDSElement.id).all()

        return edstempelements

    def getConfESSource(self, id_ver, db, log):

        if (db == None or id_ver == -2):
            log.error('ERROR: getConfESSource - input parameters error')

        ess = db.query(ESSource).from_statement(
            text(" SELECT u_essources.id, u_essources.id_template, u_essources.name "
                 + "FROM u_essources, u_conf2ess "
                 + "WHERE u_conf2ess.id_essource=u_essources.id "
                 + "and u_conf2ess.id_confver =:ver  ")).params(ver=id_ver).all()
        return ess

    def getESSTemplates(self, id_rel, db, log):

        if (db == None or id_rel == -2):
            log.error('ERROR: getESSTemplates - input parameters error')

        essTemp = db.query(ESSourceTemplate).from_statement(text("select u_esstemplates.id, u_esstemplates.name "
                                                                 + "FROM u_esstemplates, u_esst2rele "
                                                                 + "WHERE u_esst2rele.id_release=:id_rel "
                                                                 + "and u_esstemplates.id = u_esst2rele.id_esstemplate")).params(
            id_rel=id_rel).all()

        return essTemp

    def getConfToESSRel(self, id_ver, db, log):

        if (db == None or id_ver == -2):
            log.error('ERROR: getConfToESSRel - input parameters error')

        essources = db.query(ConfToEss).from_statement(
            text(" SELECT u_conf2ess.id, u_conf2ess.id_essource, u_conf2ess.ord "
                 + "FROM u_conf2ess "
                 + "WHERE u_conf2ess.id_confver =:ver ")).params(ver=id_ver).all()

        return essources

    def getESSTemplateByEss(self, id_ess, db, log):

        if (db == None or id_ess == -2):
            log.error('ERROR: getESSTemplateByEss - input parameters error')

        esSrcTemp = db.query(ESSourceTemplate).from_statement(text("select u_esstemplates.id, u_esstemplates.name "
                                                                   + "FROM u_esstemplates, u_essources "
                                                                   + "WHERE u_essources.id_template=u_esstemplates.id "
                                                                   + "AND u_essources.id=:id_ess")).params(
            id_ess=id_ess).first()

        return esSrcTemp

    def getESSTemplateParams(self, id_templ, db, log):

        if (id_templ == -2 or db == None):
            log.error('ERROR: getESSTemplateParams - input parameters error')

        esstempelements = db.query(ESSTempElement).filter(ESSTempElement.id_esstemplate == id_templ).order_by(
            ESSTempElement.id).all()

        return esstempelements

    def getESSourceParams(self, id_eds, db, log):

        if (id_eds == -2 or db == None):
            log.error('ERROR: getESSourceParams - input parameters error')

        esstempelements = db.query(ESSElement).filter(ESSElement.id_essource == id_eds).order_by(ESSElement.id).all()

        return esstempelements

    def getPrescaleTemplate(self, id_release, db, log):
        if (db == None or id_release == -2):
            log.error('ERROR: getSrvTemplateBySrv - input parameters error')

        prescaleTemplate = db.query(SrvTemplate).filter(SrvTemplate.name == 'PrescaleService').filter(
            Srvt2Rele.id_srvtemplate == SrvTemplate.id).filter(Srvt2Rele.id_release == id_release).first()

        return prescaleTemplate

    def getPrescale(self, id_ver, id_preTemp, db, log):
        if (db == None or id_ver == -2 or id_preTemp == -2):
            log.error('ERROR: getPrescale - input parameters error')

        prescale = db.query(Service).filter(Service.id_template == id_preTemp).filter(
            Conf2Srv.id_confver == id_ver).filter(Conf2Srv.id_service == Service.id).first()

        return prescale

    def getPrescalelabels(self, id_prescale, db, log):
        if (db == None or id_prescale == -2):
            log.error('ERROR: getPrescalelabels - input parameters error')

        prescaleLabels = db.query(SrvElement).filter(SrvElement.name == 'lvl1Labels').filter(
            SrvElement.id_service == id_prescale).first()

        return prescaleLabels

    def getAllDatsPatsRels(self, ver, idis, db, log):

        if (db == None or ver == -2 or idis == None):
            log.error('ERROR: getAllDatsPatsRels - input parameters error')

        # dprels = db.query(PathidToStrDst).filter(PathidToStrDst.id_datasetid.in_(idis)).all()
        dprels = db.query(func.max(PathidToStrDst.id), PathidToStrDst.id_datasetid, PathidToStrDst.id_pathid).filter(
            PathidToStrDst.id_datasetid.in_(idis)).group_by(PathidToStrDst.id_datasetid, PathidToStrDst.id_pathid).all()

        return dprels

    def getL1SeedsPathItems(self, idis, db, log):

        if (db == None or idis == None):
            log.error('ERROR: getL1SeedsPathItems - input parameters error')

        l1s_items = db.query(Pathitems).filter(ModToTemp.id_templ == ModTemplate.id).filter(
            or_(ModTemplate.name == 'HLTLevel1GTSeed', ModTemplate.name == 'HLTL1TSeed')).filter(
            ModToTemp.id_pae == Pathitems.id_pae).filter(Pathitems.id_pathid.in_(idis)).order_by(
            Pathitems.id_pathid).all()

        return l1s_items

    def getL1SeedsParams(self, idis, db, log):

        if (db == None or idis == None):
            log.error('ERROR: getL1SeedsParams - input parameters error')

        l1s_params = db.query(Moduleitem).filter(Moduleitem.id_moe == Modelement.id).filter(
            or_(Modelement.name == 'L1SeedsLogicalExpression', Modelement.name == 'L1TechTriggerSeeding')).filter(
            Moduleitem.id_pae.in_(idis)).all()

        return l1s_params

    def getL1SeedsTemplate(self, id_rel, db, log):

        if (db == None or id_rel == None):
            log.error('ERROR: getL1SeedsTemplate - input parameters error')

        l1s_temp = db.query(ModTemplate).filter(
            or_(ModTemplate.name == 'HLTLevel1GTSeed', ModTemplate.name == 'HLTL1TSeed')).filter(
            ModTemp2Rele.id_modtemp == ModTemplate.id).filter(ModTemp2Rele.id_release == id_rel).first()

        return l1s_temp

    def getL1SeedsTempParams(self, id_temp, db, log):

        if (db == None or id_temp == -2):
            log.error('ERROR: getL1SeedsTempParams - input parameters error')

        l1s_temp_params = db.query(ModTelement).filter(
            or_(ModTelement.name == 'L1SeedsLogicalExpression', ModTelement.name == 'L1TechTriggerSeeding')).filter(
            ModTelement.id_modtemp == id_temp).all()

        return l1s_temp_params

    def getPathidToOum(self, streams, db, log):

        if (db == None or streams == None):
            log.error('ERROR: getPathidToOum - input parameters error')

        pidToum = db.query(PathidToOutM).filter(PathidToOutM.id_streamid.in_(streams)).all()

        return pidToum

    def getSmartPrescaleModule(self, ver_id, id_rel, paths, db, log):

        if (db == None or paths == None or ver_id == -1 or id_rel == -1):
            log.error('ERROR: getSmartPrescaleModule - input parameters error')

        smMods = db.query(Pathitems).filter(Pathitems.id_pathid == Pathidconf.id_pathid).filter(
            Pathidconf.id_confver == ver_id).filter(Pathitems.id_pathid.in_(paths)).filter(
            Pathitems.id_pae == ModToTemp.id_pae).filter(ModToTemp.id_templ == ModTemplate.id).filter(
            ModTemplate.name == 'TriggerResultsFilter').filter(ModTemp2Rele.id_modtemp == ModTemplate.id).filter(
            ModTemp2Rele.id_release == id_rel).all()

        return smMods

    def getSmartPrescaleExpressions(self, mods, db, log):
        if (db == None or mods == None):
            log.error('ERROR: getSmartPrescaleExpressions - input parameters error')

        smExps = db.query(Moduleitem).filter(Moduleitem.id_pae.in_(mods)).filter(
            Moduleitem.id_moe == Modelement.id).filter(Modelement.name == 'triggerConditions').all()

        return smExps

    def getModules(self, id_ver, db, log):

        if (id_ver == -2 or db == None):
            log.error('ERROR: getModules - input parameters error')

        query = db.query(PathelementFull).from_statement(text("""SELECT DISTINCT
                u_paelements.id AS id,
                u_paelements.name AS name,
                u_paelements.paetype AS paetype,
                u_mod2templ.id_templ AS id_templ,
                u_moduletemplates.name AS temp_name,
                u_moduletypes.type AS mtype
            FROM
                u_mod2templ,
                u_moduletemplates,
                u_modt2rele,
                u_confversions,
                u_moduletypes,
                u_paelements,
                u_pathid2pae,
                u_pathid2conf
            WHERE
                u_moduletypes.id = u_moduletemplates.id_mtype
            AND u_moduletemplates.id = u_modt2rele.id_modtemplate
            AND u_modt2rele.id_release = u_confversions.id_release
            AND u_confversions.id = :version
            AND u_moduletemplates.id = u_mod2templ.id_templ
            AND u_mod2templ.id_pae = u_paelements.id
            AND u_paelements.paetype = 1
            AND u_paelements.id = u_pathid2pae.id_pae
            AND u_pathid2pae.id_pathid = u_pathid2conf.id_pathid
            AND u_pathid2conf.id_confver = :version
            ORDER BY name""")).params(version=id_ver)
        elements = query.all()

        return elements

    def getModuleTemplateParameters(self, id_rel, db, log):

        if (id_rel == -2 or db == None):
            log.error('ERROR: getModuleTemplateParameters - input parameters error')

        query = db.query(ModTelement).filter(ModTelement.id_modtemp == ModTemp2Rele.id_modtemp).filter(
            ModTemp2Rele.id_release == id_rel)

        elements = query.all()

        return elements

    def getRelease(self, id_rel, db, log):

        if (id_rel == -2 or db == None):
            log.error('ERROR: getRelease - input parameters error')

        query = db.query(Release).filter(Release.id == id_rel)

        elements = query.first()

        return elements

    def getConfigurationByName(self, name, db, log):
        if (db == None or name == ""):
            log.error('ERROR: getConfigurationByName - input parameters error')
            return None

        confVer = db.query(Version).filter(Version.name == name).first()

        return confVer.id

    # Returns the module "HtlPrescaler" from an End Path if present
    # @params:
    #         
    #     id_pathid: id of the end path table in the confDB
    #     db: database session object
    #
    def getEndPathPrescaleMod(self, id_pathid=None, db=None, log=None):

        if (db == None or id_pathid == None):
            log.error('ERROR: getEndPathPrescaleMod - input parameters error')

        ep_pre_mod = db.query(Pathitems).filter(ModToTemp.id_templ == ModTemplate.id).filter(
            ModTemplate.name == 'HLTPrescaler').filter(ModToTemp.id_pae == Pathitems.id_pae).filter(
            Pathitems.id_pathid == id_pathid).order_by(Pathitems.id_pathid).all()

        return ep_pre_mod

    # Returns the Endpaths from a SET of Streams
    # @params:
    #         
    #         ver_id: id of the ConfVersion
    #         idis: list of streamids 
    #         db: database session object
    #
    def getEndPathsFromStreams(self, ver_id, idis, db, log):

        if (ver_id == -2 or db == None):
            log.error('ERROR: getEndPathsFromStreams - input parameters error')

        endpaths = db.query(Pathids).filter(PathidToOutM.id_streamid.in_(idis)).filter(
            PathidToOutM.id_pathid == Pathids.id).filter(Pathids.isEndPath == 1).all()

        return endpaths

    # Returns the relations between Streamids and output modules and end paths for a SET of Streams
    # @params:
    #         
    #     ver_id: id of the ConfVersion
    #     idis: list of streamids 
    #     db: database session object
    #
    def getOumStreamRels(self, ver_id, idis, db, log):

        if (ver_id == -2 or db == None):
            log.error('ERROR: getOumStreamRels - input parameters error')

        query = db.query(func.max(PathidToOutM.id), PathidToOutM.id_streamid, PathidToOutM.id_pathid).filter(
            PathidToOutM.id_streamid.in_(idis)).group_by(PathidToOutM.id_streamid, PathidToOutM.id_pathid)
        rels = query.all()

        return rels

        # Returns the id of the Configuration quieried on its name

    # @params:
    #
    #     name: name of the Configuration to retreive
    #     
    #     db: database session object
    #
    def getMenuByName(self, name="", db=None, log=None):
        if (db == None or name == ""):
            log.error('ERROR: getMenuByName - input parameters error')
            return None

        conf = db.query(Configuration).filter(Configuration.name == name).first()

        print "RESULT CNF: " + str(conf)

        return conf.id

    def save_version(self, version, db=None, log=None):
        if db is None or version is None:
            log.error('ERROR: save_version - input parameters error')
        db.query(Version).filter_by(creator='admin').delete()
        return self.save_obj(version, db, log)

    def save_get_id_mapping(self, obj_array, db=None, log=None):
        old2new = OrderedDict()
        if db is None or obj_array is None or len(obj_array) is 0:
            log.error('ERROR: save_get_id_mapping - input parameters error')
        else:
            for obj in obj_array:
                tmp_old_id = obj.id
                self.detach_obj_from_session(obj, db, log)
                db.add(obj)
                db.flush()
                old2new[tmp_old_id] = obj.id
        return old2new

    @staticmethod
    def save_obj(obj, db=None, log=None):
        if db is None or obj is None:
            log.error('ERROR: save_obj - input parameters error')
            return None
        else:
            db.add(obj)
            db.flush()
            return obj

    @staticmethod
    def save_objects(obj_array, db=None, log=None):
        if db is None or obj_array is None or len(obj_array) is 0:
            log.error('ERROR: save_and_detach_objects - input parameters error')
        else:
            db.bulk_save_objects(obj_array)

    @staticmethod
    def detach_obj_from_session(obj, db=None, log=None):
        if db is None or obj is None:
            log.error('ERROR: detach_obj_from_session - input parameters error')
        else:
            obj.id = None
            db.expunge(obj)
            make_transient(obj)

    def detach_objects_from_session(self, obj_array, db=None, log=None):
        if db is None or obj_array is None or len(obj_array) is 0:
            log.error('ERROR: detach_objects_from_session - input parameters error')
        else:
            for obj in obj_array:
                self.detach_obj_from_session(obj, db, log)

    #for testing only
    def cleanup(self, db, ver_id):
        print ver_id
        db.query(Version).filter_by(id=ver_id, creator='admin').delete()
            # for path_id in path_ids_to_delete:
            #     db.query(Pathids).filter_by(id=path_id).delete()
            # print db.query(Pathidconf).filter_by(id_confver=ver_id).delete()
        db.commit()


