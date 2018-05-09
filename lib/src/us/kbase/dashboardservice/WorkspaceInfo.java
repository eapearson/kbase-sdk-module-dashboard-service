
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
 * <p>Original spec-file type: WorkspaceInfo</p>
 * <pre>
 * Restructured workspace info 'wsInfo' tuple:
 * id: wsInfo[0],
 * name: wsInfo[1],
 * owner: wsInfo[2],
 * moddate: wsInfo[3],
 * object_count: wsInfo[4],
 * user_permission: wsInfo[5],
 * globalread: wsInfo[6],
 * lockstat: wsInfo[7],
 * metadata: wsInfo[8],
 * modDateMs: ServiceUtils.iso8601ToMillisSinceEpoch(wsInfo[3])
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "id",
    "name",
    "owner",
    "moddate",
    "object_count",
    "user_permission",
    "globalread",
    "lockstat",
    "metadata",
    "modDateMs"
})
public class WorkspaceInfo {

    @JsonProperty("id")
    private Long id;
    @JsonProperty("name")
    private java.lang.String name;
    @JsonProperty("owner")
    private java.lang.String owner;
    @JsonProperty("moddate")
    private java.lang.String moddate;
    @JsonProperty("object_count")
    private Long objectCount;
    @JsonProperty("user_permission")
    private java.lang.String userPermission;
    @JsonProperty("globalread")
    private java.lang.String globalread;
    @JsonProperty("lockstat")
    private java.lang.String lockstat;
    @JsonProperty("metadata")
    private Map<String, String> metadata;
    @JsonProperty("modDateMs")
    private Long modDateMs;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("id")
    public Long getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(Long id) {
        this.id = id;
    }

    public WorkspaceInfo withId(Long id) {
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

    public WorkspaceInfo withName(java.lang.String name) {
        this.name = name;
        return this;
    }

    @JsonProperty("owner")
    public java.lang.String getOwner() {
        return owner;
    }

    @JsonProperty("owner")
    public void setOwner(java.lang.String owner) {
        this.owner = owner;
    }

    public WorkspaceInfo withOwner(java.lang.String owner) {
        this.owner = owner;
        return this;
    }

    @JsonProperty("moddate")
    public java.lang.String getModdate() {
        return moddate;
    }

    @JsonProperty("moddate")
    public void setModdate(java.lang.String moddate) {
        this.moddate = moddate;
    }

    public WorkspaceInfo withModdate(java.lang.String moddate) {
        this.moddate = moddate;
        return this;
    }

    @JsonProperty("object_count")
    public Long getObjectCount() {
        return objectCount;
    }

    @JsonProperty("object_count")
    public void setObjectCount(Long objectCount) {
        this.objectCount = objectCount;
    }

    public WorkspaceInfo withObjectCount(Long objectCount) {
        this.objectCount = objectCount;
        return this;
    }

    @JsonProperty("user_permission")
    public java.lang.String getUserPermission() {
        return userPermission;
    }

    @JsonProperty("user_permission")
    public void setUserPermission(java.lang.String userPermission) {
        this.userPermission = userPermission;
    }

    public WorkspaceInfo withUserPermission(java.lang.String userPermission) {
        this.userPermission = userPermission;
        return this;
    }

    @JsonProperty("globalread")
    public java.lang.String getGlobalread() {
        return globalread;
    }

    @JsonProperty("globalread")
    public void setGlobalread(java.lang.String globalread) {
        this.globalread = globalread;
    }

    public WorkspaceInfo withGlobalread(java.lang.String globalread) {
        this.globalread = globalread;
        return this;
    }

    @JsonProperty("lockstat")
    public java.lang.String getLockstat() {
        return lockstat;
    }

    @JsonProperty("lockstat")
    public void setLockstat(java.lang.String lockstat) {
        this.lockstat = lockstat;
    }

    public WorkspaceInfo withLockstat(java.lang.String lockstat) {
        this.lockstat = lockstat;
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

    public WorkspaceInfo withMetadata(Map<String, String> metadata) {
        this.metadata = metadata;
        return this;
    }

    @JsonProperty("modDateMs")
    public Long getModDateMs() {
        return modDateMs;
    }

    @JsonProperty("modDateMs")
    public void setModDateMs(Long modDateMs) {
        this.modDateMs = modDateMs;
    }

    public WorkspaceInfo withModDateMs(Long modDateMs) {
        this.modDateMs = modDateMs;
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
        return ((((((((((((((((((((((("WorkspaceInfo"+" [id=")+ id)+", name=")+ name)+", owner=")+ owner)+", moddate=")+ moddate)+", objectCount=")+ objectCount)+", userPermission=")+ userPermission)+", globalread=")+ globalread)+", lockstat=")+ lockstat)+", metadata=")+ metadata)+", modDateMs=")+ modDateMs)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
