
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
 * <p>Original spec-file type: ListAllNarrativesParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "just_modified_after"
})
public class ListAllNarrativesParams {

    @JsonProperty("just_modified_after")
    private String justModifiedAfter;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("just_modified_after")
    public String getJustModifiedAfter() {
        return justModifiedAfter;
    }

    @JsonProperty("just_modified_after")
    public void setJustModifiedAfter(String justModifiedAfter) {
        this.justModifiedAfter = justModifiedAfter;
    }

    public ListAllNarrativesParams withJustModifiedAfter(String justModifiedAfter) {
        this.justModifiedAfter = justModifiedAfter;
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
        return ((((("ListAllNarrativesParams"+" [justModifiedAfter=")+ justModifiedAfter)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
