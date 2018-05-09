
package us.kbase.dashboardservice;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.common.service.Tuple11;
import us.kbase.common.service.Tuple9;


/**
 * <p>Original spec-file type: Narrative</p>
 * <pre>
 * Listing Narratives / Naratorials (plus Narratorial Management)
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "ws",
    "nar"
})
public class Narrative {

    @JsonProperty("ws")
    private Tuple9 <Long, String, String, String, Long, String, String, String, Map<String, String>> ws;
    @JsonProperty("nar")
    private Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>> nar;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("ws")
    public Tuple9 <Long, String, String, String, Long, String, String, String, Map<String, String>> getWs() {
        return ws;
    }

    @JsonProperty("ws")
    public void setWs(Tuple9 <Long, String, String, String, Long, String, String, String, Map<String, String>> ws) {
        this.ws = ws;
    }

    public Narrative withWs(Tuple9 <Long, String, String, String, Long, String, String, String, Map<String, String>> ws) {
        this.ws = ws;
        return this;
    }

    @JsonProperty("nar")
    public Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>> getNar() {
        return nar;
    }

    @JsonProperty("nar")
    public void setNar(Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>> nar) {
        this.nar = nar;
    }

    public Narrative withNar(Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>> nar) {
        this.nar = nar;
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
        return ((((((("Narrative"+" [ws=")+ ws)+", nar=")+ nar)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
