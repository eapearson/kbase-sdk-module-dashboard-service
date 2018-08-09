
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
 * <p>Original spec-file type: CreateNarrativeResult</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "narrative"
})
public class CreateNarrativeResult {

    /**
     * <p>Original spec-file type: Narrative</p>
     * 
     * 
     */
    @JsonProperty("narrative")
    private Narrative narrative;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
     * <p>Original spec-file type: Narrative</p>
     * 
     * 
     */
    @JsonProperty("narrative")
    public Narrative getNarrative() {
        return narrative;
    }

    /**
     * <p>Original spec-file type: Narrative</p>
     * 
     * 
     */
    @JsonProperty("narrative")
    public void setNarrative(Narrative narrative) {
        this.narrative = narrative;
    }

    public CreateNarrativeResult withNarrative(Narrative narrative) {
        this.narrative = narrative;
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
        return ((((("CreateNarrativeResult"+" [narrative=")+ narrative)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
