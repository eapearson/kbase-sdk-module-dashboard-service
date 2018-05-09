
package us.kbase.dashboardservice;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: ObjectInfo</p>
 * <pre>
 * Restructured workspace object info 'data' tuple:
 * id: data[0],
 * name: data[1],
 * type: data[2],
 * save_date: data[3],
 * version: data[4],
 * saved_by: data[5],
 * wsid: data[6],
 * ws: data[7],
 * checksum: data[8],
 * size: data[9],
 * metadata: data[10],
 * ref: data[6] + '/' + data[0] + '/' + data[4],
 * obj_id: 'ws.' + data[6] + '.obj.' + data[0],
 * typeModule: type[0],
 * typeName: type[1],
 * typeMajorVersion: type[2],
 * typeMinorVersion: type[3],
 * saveDateMs: ServiceUtils.iso8601ToMillisSinceEpoch(data[3])
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "id",
    "name",
    "type",
    "save_date",
    "version",
    "saved_by",
    "wsid",
    "ws",
    "checksum",
    "size",
    "metadata",
    "ref",
    "obj_id",
    "typeModule",
    "typeName",
    "typeMajorVersion",
    "typeMinorVersion",
    "saveDateMs"
})
public class ObjectInfo {

    @JsonProperty("id")
    private Long id;
    @JsonProperty("name")
    private java.lang.String name;
    @JsonProperty("type")
    private java.lang.String type;
    @JsonProperty("save_date")
    private java.lang.String saveDate;
    @JsonProperty("version")
    private Long version;
    @JsonProperty("saved_by")
    private java.lang.String savedBy;
    @JsonProperty("wsid")
    private Long wsid;
    @JsonProperty("ws")
    private java.lang.String ws;
    @JsonProperty("checksum")
    private java.lang.String checksum;
    @JsonProperty("size")
    private Long size;
    @JsonProperty("metadata")
    private Map<String, String> metadata;
    @JsonProperty("ref")
    private java.lang.String ref;
    @JsonProperty("obj_id")
    private java.lang.String objId;
    @JsonProperty("typeModule")
    private java.lang.String typeModule;
    @JsonProperty("typeName")
    private java.lang.String typeName;
    @JsonProperty("typeMajorVersion")
    private java.lang.String typeMajorVersion;
    @JsonProperty("typeMinorVersion")
    private java.lang.String typeMinorVersion;
    @JsonProperty("saveDateMs")
    private Long saveDateMs;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("id")
    public Long getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(Long id) {
        this.id = id;
    }

    public ObjectInfo withId(Long id) {
        this.id = id;
        return this;
    }

    @JsonProperty("name")
    public java.lang.String getName() {
        return name;
    }

    @JsonProperty("name")
    public void setName(java.lang.String name) {
        this.name = name;
    }

    public ObjectInfo withName(java.lang.String name) {
        this.name = name;
        return this;
    }

    @JsonProperty("type")
    public java.lang.String getType() {
        return type;
    }

    @JsonProperty("type")
    public void setType(java.lang.String type) {
        this.type = type;
    }

    public ObjectInfo withType(java.lang.String type) {
        this.type = type;
        return this;
    }

    @JsonProperty("save_date")
    public java.lang.String getSaveDate() {
        return saveDate;
    }

    @JsonProperty("save_date")
    public void setSaveDate(java.lang.String saveDate) {
        this.saveDate = saveDate;
    }

    public ObjectInfo withSaveDate(java.lang.String saveDate) {
        this.saveDate = saveDate;
        return this;
    }

    @JsonProperty("version")
    public Long getVersion() {
        return version;
    }

    @JsonProperty("version")
    public void setVersion(Long version) {
        this.version = version;
    }

    public ObjectInfo withVersion(Long version) {
        this.version = version;
        return this;
    }

    @JsonProperty("saved_by")
    public java.lang.String getSavedBy() {
        return savedBy;
    }

    @JsonProperty("saved_by")
    public void setSavedBy(java.lang.String savedBy) {
        this.savedBy = savedBy;
    }

    public ObjectInfo withSavedBy(java.lang.String savedBy) {
        this.savedBy = savedBy;
        return this;
    }

    @JsonProperty("wsid")
    public Long getWsid() {
        return wsid;
    }

    @JsonProperty("wsid")
    public void setWsid(Long wsid) {
        this.wsid = wsid;
    }

    public ObjectInfo withWsid(Long wsid) {
        this.wsid = wsid;
        return this;
    }

    @JsonProperty("ws")
    public java.lang.String getWs() {
        return ws;
    }

    @JsonProperty("ws")
    public void setWs(java.lang.String ws) {
        this.ws = ws;
    }

    public ObjectInfo withWs(java.lang.String ws) {
        this.ws = ws;
        return this;
    }

    @JsonProperty("checksum")
    public java.lang.String getChecksum() {
        return checksum;
    }

    @JsonProperty("checksum")
    public void setChecksum(java.lang.String checksum) {
        this.checksum = checksum;
    }

    public ObjectInfo withChecksum(java.lang.String checksum) {
        this.checksum = checksum;
        return this;
    }

    @JsonProperty("size")
    public Long getSize() {
        return size;
    }

    @JsonProperty("size")
    public void setSize(Long size) {
        this.size = size;
    }

    public ObjectInfo withSize(Long size) {
        this.size = size;
        return this;
    }

    @JsonProperty("metadata")
    public Map<String, String> getMetadata() {
        return metadata;
    }

    @JsonProperty("metadata")
    public void setMetadata(Map<String, String> metadata) {
        this.metadata = metadata;
    }

    public ObjectInfo withMetadata(Map<String, String> metadata) {
        this.metadata = metadata;
        return this;
    }

    @JsonProperty("ref")
    public java.lang.String getRef() {
        return ref;
    }

    @JsonProperty("ref")
    public void setRef(java.lang.String ref) {
        this.ref = ref;
    }

    public ObjectInfo withRef(java.lang.String ref) {
        this.ref = ref;
        return this;
    }

    @JsonProperty("obj_id")
    public java.lang.String getObjId() {
        return objId;
    }

    @JsonProperty("obj_id")
    public void setObjId(java.lang.String objId) {
        this.objId = objId;
    }

    public ObjectInfo withObjId(java.lang.String objId) {
        this.objId = objId;
        return this;
    }

    @JsonProperty("typeModule")
    public java.lang.String getTypeModule() {
        return typeModule;
    }

    @JsonProperty("typeModule")
    public void setTypeModule(java.lang.String typeModule) {
        this.typeModule = typeModule;
    }

    public ObjectInfo withTypeModule(java.lang.String typeModule) {
        this.typeModule = typeModule;
        return this;
    }

    @JsonProperty("typeName")
    public java.lang.String getTypeName() {
        return typeName;
    }

    @JsonProperty("typeName")
    public void setTypeName(java.lang.String typeName) {
        this.typeName = typeName;
    }

    public ObjectInfo withTypeName(java.lang.String typeName) {
        this.typeName = typeName;
        return this;
    }

    @JsonProperty("typeMajorVersion")
    public java.lang.String getTypeMajorVersion() {
        return typeMajorVersion;
    }

    @JsonProperty("typeMajorVersion")
    public void setTypeMajorVersion(java.lang.String typeMajorVersion) {
        this.typeMajorVersion = typeMajorVersion;
    }

    public ObjectInfo withTypeMajorVersion(java.lang.String typeMajorVersion) {
        this.typeMajorVersion = typeMajorVersion;
        return this;
    }

    @JsonProperty("typeMinorVersion")
    public java.lang.String getTypeMinorVersion() {
        return typeMinorVersion;
    }

    @JsonProperty("typeMinorVersion")
    public void setTypeMinorVersion(java.lang.String typeMinorVersion) {
        this.typeMinorVersion = typeMinorVersion;
    }

    public ObjectInfo withTypeMinorVersion(java.lang.String typeMinorVersion) {
        this.typeMinorVersion = typeMinorVersion;
        return this;
    }

    @JsonProperty("saveDateMs")
    public Long getSaveDateMs() {
        return saveDateMs;
    }

    @JsonProperty("saveDateMs")
    public void setSaveDateMs(Long saveDateMs) {
        this.saveDateMs = saveDateMs;
    }

    public ObjectInfo withSaveDateMs(Long saveDateMs) {
        this.saveDateMs = saveDateMs;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((((((((((((((((((((((((((((((("ObjectInfo"+" [id=")+ id)+", name=")+ name)+", type=")+ type)+", saveDate=")+ saveDate)+", version=")+ version)+", savedBy=")+ savedBy)+", wsid=")+ wsid)+", ws=")+ ws)+", checksum=")+ checksum)+", size=")+ size)+", metadata=")+ metadata)+", ref=")+ ref)+", objId=")+ objId)+", typeModule=")+ typeModule)+", typeName=")+ typeName)+", typeMajorVersion=")+ typeMajorVersion)+", typeMinorVersion=")+ typeMinorVersion)+", saveDateMs=")+ saveDateMs)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
