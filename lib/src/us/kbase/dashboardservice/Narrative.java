
package us.kbase.dashboardservice;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.common.service.UObject;


/**
 * <p>Original spec-file type: Narrative</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "objectId",
    "objectVersion",
    "owner",
    "permission",
    "isPublic",
    "isNarratorial",
    "title",
    "savedTime",
    "savedBy",
    "permissions",
    "cellTypes",
    "apps"
})
public class Narrative {

    @JsonProperty("objectId")
    private Long objectId;
    @JsonProperty("objectVersion")
    private Long objectVersion;
    @JsonProperty("owner")
    private String owner;
    @JsonProperty("permission")
    private String permission;
    @JsonProperty("isPublic")
    private Long isPublic;
    @JsonProperty("isNarratorial")
    private Long isNarratorial;
    @JsonProperty("title")
    private String title;
    @JsonProperty("savedTime")
    private Long savedTime;
    @JsonProperty("savedBy")
    private String savedBy;
    @JsonProperty("permissions")
    private List<UserPermission> permissions;
    @JsonProperty("cellTypes")
    private List<UObject> cellTypes;
    @JsonProperty("apps")
    private List<UObject> apps;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("objectId")
    public Long getObjectId() {
        return objectId;
    }

    @JsonProperty("objectId")
    public void setObjectId(Long objectId) {
        this.objectId = objectId;
    }

    public Narrative withObjectId(Long objectId) {
        this.objectId = objectId;
        return this;
    }

    @JsonProperty("objectVersion")
    public Long getObjectVersion() {
        return objectVersion;
    }

    @JsonProperty("objectVersion")
    public void setObjectVersion(Long objectVersion) {
        this.objectVersion = objectVersion;
    }

    public Narrative withObjectVersion(Long objectVersion) {
        this.objectVersion = objectVersion;
        return this;
    }

    @JsonProperty("owner")
    public String getOwner() {
        return owner;
    }

    @JsonProperty("owner")
    public void setOwner(String owner) {
        this.owner = owner;
    }

    public Narrative withOwner(String owner) {
        this.owner = owner;
        return this;
    }

    @JsonProperty("permission")
    public String getPermission() {
        return permission;
    }

    @JsonProperty("permission")
    public void setPermission(String permission) {
        this.permission = permission;
    }

    public Narrative withPermission(String permission) {
        this.permission = permission;
        return this;
    }

    @JsonProperty("isPublic")
    public Long getIsPublic() {
        return isPublic;
    }

    @JsonProperty("isPublic")
    public void setIsPublic(Long isPublic) {
        this.isPublic = isPublic;
    }

    public Narrative withIsPublic(Long isPublic) {
        this.isPublic = isPublic;
        return this;
    }

    @JsonProperty("isNarratorial")
    public Long getIsNarratorial() {
        return isNarratorial;
    }

    @JsonProperty("isNarratorial")
    public void setIsNarratorial(Long isNarratorial) {
        this.isNarratorial = isNarratorial;
    }

    public Narrative withIsNarratorial(Long isNarratorial) {
        this.isNarratorial = isNarratorial;
        return this;
    }

    @JsonProperty("title")
    public String getTitle() {
        return title;
    }

    @JsonProperty("title")
    public void setTitle(String title) {
        this.title = title;
    }

    public Narrative withTitle(String title) {
        this.title = title;
        return this;
    }

    @JsonProperty("savedTime")
    public Long getSavedTime() {
        return savedTime;
    }

    @JsonProperty("savedTime")
    public void setSavedTime(Long savedTime) {
        this.savedTime = savedTime;
    }

    public Narrative withSavedTime(Long savedTime) {
        this.savedTime = savedTime;
        return this;
    }

    @JsonProperty("savedBy")
    public String getSavedBy() {
        return savedBy;
    }

    @JsonProperty("savedBy")
    public void setSavedBy(String savedBy) {
        this.savedBy = savedBy;
    }

    public Narrative withSavedBy(String savedBy) {
        this.savedBy = savedBy;
        return this;
    }

    @JsonProperty("permissions")
    public List<UserPermission> getPermissions() {
        return permissions;
    }

    @JsonProperty("permissions")
    public void setPermissions(List<UserPermission> permissions) {
        this.permissions = permissions;
    }

    public Narrative withPermissions(List<UserPermission> permissions) {
        this.permissions = permissions;
        return this;
    }

    @JsonProperty("cellTypes")
    public List<UObject> getCellTypes() {
        return cellTypes;
    }

    @JsonProperty("cellTypes")
    public void setCellTypes(List<UObject> cellTypes) {
        this.cellTypes = cellTypes;
    }

    public Narrative withCellTypes(List<UObject> cellTypes) {
        this.cellTypes = cellTypes;
        return this;
    }

    @JsonProperty("apps")
    public List<UObject> getApps() {
        return apps;
    }

    @JsonProperty("apps")
    public void setApps(List<UObject> apps) {
        this.apps = apps;
    }

    public Narrative withApps(List<UObject> apps) {
        this.apps = apps;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((((((((((((((("Narrative"+" [objectId=")+ objectId)+", objectVersion=")+ objectVersion)+", owner=")+ owner)+", permission=")+ permission)+", isPublic=")+ isPublic)+", isNarratorial=")+ isNarratorial)+", title=")+ title)+", savedTime=")+ savedTime)+", savedBy=")+ savedBy)+", permissions=")+ permissions)+", cellTypes=")+ cellTypes)+", apps=")+ apps)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
