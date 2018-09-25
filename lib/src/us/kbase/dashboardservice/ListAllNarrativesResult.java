
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
 * <p>Original spec-file type: ListAllNarrativesResult</p>
 * <pre>
 * typedef structure {
 * workspace_info workspace;
 * object_info object;
 * list<UserPermission> permissions;
 *     } NarrativeX;
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "narratives",
    "profiles",
    "apps"
})
public class ListAllNarrativesResult {

    @JsonProperty("narratives")
    private List<Narrative> narratives;
    @JsonProperty("profiles")
    private Map<String, UObject> profiles;
    @JsonProperty("apps")
    private Map<String, App> apps;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("narratives")
    public List<Narrative> getNarratives() {
        return narratives;
    }

    @JsonProperty("narratives")
    public void setNarratives(List<Narrative> narratives) {
        this.narratives = narratives;
    }

    public ListAllNarrativesResult withNarratives(List<Narrative> narratives) {
        this.narratives = narratives;
        return this;
    }

    @JsonProperty("profiles")
    public Map<String, UObject> getProfiles() {
        return profiles;
    }

    @JsonProperty("profiles")
    public void setProfiles(Map<String, UObject> profiles) {
        this.profiles = profiles;
    }

    public ListAllNarrativesResult withProfiles(Map<String, UObject> profiles) {
        this.profiles = profiles;
        return this;
    }

    @JsonProperty("apps")
    public Map<String, App> getApps() {
        return apps;
    }

    @JsonProperty("apps")
    public void setApps(Map<String, App> apps) {
        this.apps = apps;
    }

    public ListAllNarrativesResult withApps(Map<String, App> apps) {
        this.apps = apps;
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
        return ((((((((("ListAllNarrativesResult"+" [narratives=")+ narratives)+", profiles=")+ profiles)+", apps=")+ apps)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
