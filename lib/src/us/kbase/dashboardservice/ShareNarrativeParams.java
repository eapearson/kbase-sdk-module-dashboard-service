
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


/**
 * <p>Original spec-file type: ShareNarrativeParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "wsi",
    "users",
    "permission"
})
public class ShareNarrativeParams {

    /**
     * <p>Original spec-file type: WorkspaceIdentity</p>
     * 
     * 
     */
    @JsonProperty("wsi")
    private WorkspaceIdentity wsi;
    @JsonProperty("users")
    private List<String> users;
    @JsonProperty("permission")
    private java.lang.String permission;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    /**
     * <p>Original spec-file type: WorkspaceIdentity</p>
     * 
     * 
     */
    @JsonProperty("wsi")
    public WorkspaceIdentity getWsi() {
        return wsi;
    }

    /**
     * <p>Original spec-file type: WorkspaceIdentity</p>
     * 
     * 
     */
    @JsonProperty("wsi")
    public void setWsi(WorkspaceIdentity wsi) {
        this.wsi = wsi;
    }

    public ShareNarrativeParams withWsi(WorkspaceIdentity wsi) {
        this.wsi = wsi;
        return this;
    }

    @JsonProperty("users")
    public List<String> getUsers() {
        return users;
    }

    @JsonProperty("users")
    public void setUsers(List<String> users) {
        this.users = users;
    }

    public ShareNarrativeParams withUsers(List<String> users) {
        this.users = users;
        return this;
    }

    @JsonProperty("permission")
    public java.lang.String getPermission() {
        return permission;
    }

    @JsonProperty("permission")
    public void setPermission(java.lang.String permission) {
        this.permission = permission;
    }

    public ShareNarrativeParams withPermission(java.lang.String permission) {
        this.permission = permission;
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
        return ((((((((("ShareNarrativeParams"+" [wsi=")+ wsi)+", users=")+ users)+", permission=")+ permission)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
