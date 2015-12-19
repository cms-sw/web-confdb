import traceback
from item_wrappers.Parameter import *

class ParamsBuilder():

    @staticmethod
    def buildParameters(session, logger, query, module_id, set_default = False):
        # check the input parameters
        if (module_id == -2 or session == None or query == None):
            logger.error('ERROR: buildParameters - input parameters error\n' + ''.join(traceback.format_stack()))

        try:
            # retreive all the parameters of the module
            elements = query(module_id, session, logger)
        except Exception as e:
            logger.error('ERROR: query %s(%s, ...): %s' % (query.__name__, module_id, e))
            return None

        return ParamsBuilder.buildParameterStructure(logger, elements, set_default)


    @staticmethod
    def buildParameterStructure(logger, elements, set_default = False):
        # build all the parameters, PSets and VPSets
        params  = []
        level   = 0
        stack   = [ params ]
        parents = [ None ]
        prev    = None

        for p in elements:
            # build the next element
            if (p.valuelob == None or p.valuelob == "") and (p.moetype == 1):   # XXX why valuelob == "" ?  why moetype == 1 ?
                value = p.value
            else:
                value = p.valuelob

            if p.lvl > (len(stack)-1):
                assert p.lvl == len(stack)
                assert stack[-1]
                stack.append(stack[-1][-1].children)
                parents.append(prev)

            while p.lvl < (len(stack)-1):
                # stack[-1].sort(key = lambda p: p.order)
                stack.pop()
                prev = parents.pop()

            item = Parameter(p.id, p.name, value, p.moetype, p.paramtype, parents[-1], p.lvl, p.order, p.tracked, p.hex)
            item.default = set_default
            # the parameter is a PSet or VPSet
            if item.moetype == 3 or item.moetype == 2:
                item.expanded = False

            stack[-1].append(item)

            # remember the last elements as the possible next parent
            prev = p.id

        while stack:
            # stack[-1].sort(key = lambda p: p.order)
            stack.pop()

        return params


    @staticmethod
    def buildFromTemplateAndModule(session, logger, queries, module_id):
        # check the input parameters
        if (module_id == -2 or session == None or queries == None):
            logger.error('ERROR: buildFromTemplateAndModule - input parameters error\n' + ''.join(traceback.format_stack()))

        # queries = (get_template_by_module_id, get_template_parameters, get_module_parameters)
        (get_template_by_module_id, get_template_parameters, get_module_parameters) = queries

        # template DB queries
        template = None

        try:
            # find the module template
            template = get_template_by_module_id(module_id, session, logger)
        except Exception as e:
            logger.error('ERROR: query %s(%s, ...): %s' % (get_template_by_module_id.__name__, module_id, e))
            return None

        if template is None:
            logger.error('ERROR: query %s(%s, ...) did not return any values' % (get_template_by_module_id.__name__, module_id))
            return None

        # retrieve the template (default) parameters
        t_params = ParamsBuilder.buildParameters(session, logger, get_template_parameters, template.id, set_default = True)

        # retreive the module parameters
        m_params = ParamsBuilder.buildParameters(session, logger, get_module_parameters,   module_id,   set_default = False)

        # merge the template (default) and module parameters
        parameters = {}
        for p in t_params:
            parameters[p.name] = p
        for p in m_params:
            parameters[p.name] = p

        return sorted(parameters.values(), key = lambda p: p.order)


    @staticmethod
    def serviceParamsBuilder(sid = -2, queries = None, db = None, log = None):
        q = ( queries.getSrvTemplateBySrv,
              queries.getSrvTemplateParams,
              queries.getServiceParamElements )
        return ParamsBuilder.buildFromTemplateAndModule(db, log, q, sid)

    @staticmethod
    def serviceTemplateParamsBuilder(sid = -2, queries = None, db = None, log = None):
        return ParamsBuilder.buildParameters(db, log, queries.getSrvTemplateParams, sid, set_default = True)

    @staticmethod
    def moduleParamsBuilder(mid = -2, queries = None, db = None, log = None):
        q = ( queries.getTemplateFromPae,
              queries.getTemplateParams,
              queries.getModuleParamItemsOne )
        return ParamsBuilder.buildFromTemplateAndModule(db, log, q, mid)

    @staticmethod
    def esModuleParamsBuilder(sid = -2, queries = None, db = None, log = None):
        q = ( queries.getESMTemplateByEsm,
              queries.getESMTemplateParams,
              queries.getESModParams )
        return ParamsBuilder.buildFromTemplateAndModule(db, log, q, sid)

    @staticmethod
    def gpsetParamsBuilder(sid = -2, queries = None, db = None, log = None):
        return ParamsBuilder.buildParameters(db, log, queries.getGpsetElements, sid)

    @staticmethod
    def outputModuleParamsBuilder(sid = -2, queries = None, db = None, log = None):
        return ParamsBuilder.buildParameters(db, log, queries.getOUMElements, sid)

    @staticmethod
    def edSourceParamsBuilder(sid = -2, queries = None, db = None, log = None):
        q = ( queries.getEDSTemplateByEds,
              queries.getEDSTemplateParams,
              queries.getEDSourceParams )
        return ParamsBuilder.buildFromTemplateAndModule(db, log, q, sid)

    @staticmethod
    def esSourceParamsBuilder(sid = -2, queries = None, db = None, log = None):
        q = ( queries.getESSTemplateByEss,
              queries.getESSTemplateParams,
              queries.getESSourceParams )
        return ParamsBuilder.buildFromTemplateAndModule(db, log, q, sid)

