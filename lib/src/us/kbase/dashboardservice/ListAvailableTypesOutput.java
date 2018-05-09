
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
 * <p>Original spec-file type: ListAvailableTypesOutput</p>
 * <pre>
 * type_stat - number of objects by type
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "type_stat"
})
public class ListAvailableTypesOutput {

    @JsonProperty("type_stat")
    private Map<String, Long> typeStat;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("type_stat")
    public Map<String, Long> getTypeStat() {
        return typeStat;
    }

    @JsonProperty("type_stat")
    public void setTypeStat(Map<String, Long> typeStat) {
        this.typeStat = typeStat;
    }

    public ListAvailableTypesOutput withTypeStat(Map<String, Long> typeStat) {
        this.typeStat = typeStat;
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
        return ((((("ListAvailableTypesOutput"+" [typeStat=")+ typeStat)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
