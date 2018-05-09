
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
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "narratives",
    "profiles"
})
public class ListAllNarrativesResult {

    @JsonProperty("narratives")
    private List<NarrativeX> narratives;
    @JsonProperty("profiles")
    private List<UObject> profiles;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("narratives")
    public List<NarrativeX> getNarratives() {
        return narratives;
    }

    @JsonProperty("narratives")
    public void setNarratives(List<NarrativeX> narratives) {
        this.narratives = narratives;
    }

    public ListAllNarrativesResult withNarratives(List<NarrativeX> narratives) {
        this.narratives = narratives;
        return this;
    }

    @JsonProperty("profiles")
    public List<UObject> getProfiles() {
        return profiles;
    }

    @JsonProperty("profiles")
    public void setProfiles(List<UObject> profiles) {
        this.profiles = profiles;
    }

    public ListAllNarrativesResult withProfiles(List<UObject> profiles) {
        this.profiles = profiles;
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
        return ((((((("ListAllNarrativesResult"+" [narratives=")+ narratives)+", profiles=")+ profiles)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
