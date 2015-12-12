class PropertyMapper:

    def __init__(self, netcache):
        self._netcache = netcache
        self._class_to_prop_map = {}

    def get_property_name(self, archtype, prop_id):
        if archtype not in self._class_to_prop_map:
            self._class_to_prop_map[archtype] = self._build_prop_for_archtype(archtype)
        return self._class_to_prop_map[archtype][prop_id]

    def _build_prop_for_archtype(self, archtype):
        classname = self._arch_to_class(archtype)
        mapping = self._get_netprops_for_class(self._netcache, classname)
        return mapping

    def _arch_to_class(self, archname):
        # TODO Maybe there is a way to not hardcode this? I dunno
        if archname == 'GameInfo_Soccar.GameInfo.GameInfo_Soccar:GameReplicationInfoArchetype':
            classname = 'TAGame.GRI_TA'
        elif archname == 'GameInfo_Season.GameInfo.GameInfo_Season:GameReplicationInfoArchetype':
            classname = 'TAGame.GRI_TA'
        elif archname == 'Archetypes.GameEvent.GameEvent_Season:CarArchetype':
            classname = 'TAGame.Car_Season_TA'
        elif archname == 'Archetypes.Ball.CubeBall':
            classname = 'TAGame.Ball_TA'
        else:
            classname = archname.split('.')[-1].split(':')[-1]
            classname.replace("_Default", "_TA")\
                .replace("Archetype", "")\
                .replace("_0", "")\
                .replace("0", "_TA")\
                .replace("1", "_TA")\
                .replace("Default__", "")
            classname = '.' + classname
        return classname

    def _get_netprops_for_class(self, netcache, classname):
        mappings = {}
        for k, v in netcache.items():
            if type(k) == str and classname in k:
                return v['mapping']
            if type(v) == dict:
                child_map = self._get_netprops_for_class(v, classname)
                if child_map:
                    mappings = v['mapping']
                    mappings.update(child_map)
                    return mappings
        return mappings