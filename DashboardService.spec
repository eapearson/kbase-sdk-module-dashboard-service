/*
A KBase module: DashboardService
*/

module DashboardService {

    /* @range [0,1] */
    typedef int boolean;

    /*
        A time in the format YYYY-MM-DDThh:mm:ssZ, where Z is either the
        character Z (representing the UTC timezone) or the difference
        in time to UTC in the format +/-HHMM, eg:
            2012-12-17T23:24:06-0500 (EST time)
            2013-04-03T08:56:32+0000 (UTC time)
            2013-04-03T08:56:32Z (UTC time)
    */
    typedef string timestamp;

    /* Represents the permissions a user or users have to a workspace:

        'a' - administrator. All operations allowed.
        'w' - read/write.
        'r' - read.
        'n' - no permissions.
    */
    typedef string permission;

    /* The lock status of a workspace.
        One of 'unlocked', 'locked', or 'published'.
    */
    typedef string lock_status;

    /* from workspace_deluxe 
       Note too that naming conventions for paramters using these types 
       (may) also use the workspace_deluxe conventions.
    */
    typedef int ws_id;
    typedef string ws_name;
    typedef structure {
        ws_name workspace;
        ws_id id;
    } WorkspaceIdentity;

    typedef string username;



    /* Information about an object, including user provided metadata.

        obj_id objid - the numerical id of the object.
        obj_name name - the name of the object.
        type_string type - the type of the object.
        timestamp save_date - the save date of the object.
        obj_ver ver - the version of the object.
        username saved_by - the user that saved or copied the object.
        ws_id wsid - the workspace containing the object.
        ws_name workspace - the workspace containing the object.
        string chsum - the md5 checksum of the object.
        int size - the size of the object in bytes.
        usermeta meta - arbitrary user-supplied metadata about
            the object.
    */
    typedef tuple<int objid, string name, string type,
        timestamp save_date, int version, string saved_by,
        int wsid, string workspace, string chsum, int size,
        mapping<string, string> meta> object_info;

    /* Information about a workspace.

        ws_id id - the numerical ID of the workspace.
        ws_name workspace - name of the workspace.
        username owner - name of the user who owns (e.g. created) this workspace.
        timestamp moddate - date when the workspace was last modified.
        int max_objid - the maximum object ID appearing in this workspace.
            Since cloning a workspace preserves object IDs, this number may be
            greater than the number of objects in a newly cloned workspace.
        permission user_permission - permissions for the authenticated user of
            this workspace.
        permission globalread - whether this workspace is globally readable.
        lock_status lockstat - the status of the workspace lock.
        usermeta metadata - arbitrary user-supplied metadata about
            the workspace.

    */
    typedef tuple<int id, string workspace, string owner, string moddate,
        int max_objid, string user_permission, string globalread,
        string lockstat, mapping<string, string> metadata> workspace_info;

    typedef structure {
        list<object_info> set_items_info;
    } SetItems;

    /* Restructured workspace object info 'data' tuple:
        id: data[0],
        name: data[1],
        type: data[2],
        save_date: data[3],
        version: data[4],
        saved_by: data[5],
        wsid: data[6],
        ws: data[7],
        checksum: data[8],
        size: data[9],
        metadata: data[10],
        ref: data[6] + '/' + data[0] + '/' + data[4],
        obj_id: 'ws.' + data[6] + '.obj.' + data[0],
        typeModule: type[0],
        typeName: type[1],
        typeMajorVersion: type[2],
        typeMinorVersion: type[3],
        saveDateMs: ServiceUtils.iso8601ToMillisSinceEpoch(data[3])
    */
    typedef structure {
        int id;
        string name;
        string type;
        string save_date;
        int version;
        string saved_by;
        int wsid;
        string ws;
        string checksum;
        int size;
        mapping<string,string> metadata;
        string ref;
        string obj_id;
        string typeModule;
        string typeName;
        string typeMajorVersion;
        string typeMinorVersion;
        int saveDateMs;
    } ObjectInfo;

    /* Restructured workspace info 'wsInfo' tuple:
        id: wsInfo[0],
        name: wsInfo[1],
        owner: wsInfo[2],
        moddate: wsInfo[3],
        object_count: wsInfo[4],
        user_permission: wsInfo[5],
        globalread: wsInfo[6],
        lockstat: wsInfo[7],
        metadata: wsInfo[8],
        modDateMs: ServiceUtils.iso8601ToMillisSinceEpoch(wsInfo[3])
    */
    typedef structure {
        int id;
        string name;
        string owner;
        timestamp moddate;
        int object_count;
        permission user_permission;
        permission globalread;
        lock_status lockstat;
        mapping<string,string> metadata;
        int modDateMs;
    } WorkspaceInfo;

    typedef tuple<int step_pos, string key, string value> AppParam;

    /* ********************************** */
    /* Listing Narratives / Naratorials (plus Narratorial Management) */

    typedef structure {
        workspace_info ws;
        object_info nar;
    } Narrative;

    typedef structure {
        list <Narrative> narratives;
    } NarrativeList;

    /* LIST ALL NARRATIVES */

    typedef UnspecifiedObject UserProfile;

    typedef structure {
        string username;
        permission permission;
    } UserPermission;

    typedef structure {
        workspace_info ws;
        object_info nar;
        list<UserPermission> permissions;
    } NarrativeX;

    typedef structure {
        list<NarrativeX> narratives;
        list<UserProfile> profiles;
    } ListAllNarrativesResult;

    typedef structure {
    } ListAllNarrativesParams;

    typedef structure {
        list<tuple<string,int>> timings;
    } RunStats;

    funcdef list_all_narratives(ListAllNarrativesParams params)
        returns (ListAllNarrativesResult result, RunStats stats) authentication optional;

    typedef structure {
        WorkspaceIdentity wsi;
    } DeleteNarrativeParams;        

    funcdef delete_narrative(DeleteNarrativeParams params) 
        returns () authentication required;

    typedef structure {
        WorkspaceIdentity wsi;
        list<username> users;
        permission permission;
    } ShareNarrativeParams;

    funcdef share_narrative(ShareNarrativeParams params)
        returns () authentication required;

    typedef structure {
        WorkspaceIdentity wsi;
        list<username> users;
    } UnshareNarrativeParams;

    funcdef unshare_narrative(UnshareNarrativeParams params)
        returns () authentication required;

    typedef structure {
        WorkspaceIdentity wsi;
    } ShareNarrativeGlobalParams;

    funcdef share_narrative_global(ShareNarrativeGlobalParams params) 
        returns () authentication required;

    typedef structure {
        WorkspaceIdentity wsi;
    } UnshareNarrativeGlobalParams;

    funcdef unshare_narrative_global(UnshareNarrativeGlobalParams params)
        returns () authentication required;        

};
