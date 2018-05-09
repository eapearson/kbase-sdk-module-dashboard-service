
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
 * <p>Original spec-file type: NarrativeList</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "narratives"
})
public class NarrativeList {

    @JsonProperty("narratives")
    private List<Narrative> narratives;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("narratives")
    public List<Narrative> getNarratives() {
        return narratives;
    }

    @JsonProperty("narratives")
    public void setNarratives(List<Narrative> narratives) {
        this.narratives = narratives;
    }

    public NarrativeList withNarratives(List<Narrative> narratives) {
        this.narratives = narratives;
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
        return ((((("NarrativeList"+" [narratives=")+ narratives)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
