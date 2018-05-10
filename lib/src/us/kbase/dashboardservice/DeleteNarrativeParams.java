
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
 * <p>Original spec-file type: DeleteNarrativeParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "obji"
})
public class DeleteNarrativeParams {

    /**
     * <p>Original spec-file type: ObjectIdentity</p>
     * 
     * 
     */
    @JsonProperty("obji")
    private ObjectIdentity obji;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
     * <p>Original spec-file type: ObjectIdentity</p>
     * 
     * 
     */
    @JsonProperty("obji")
    public ObjectIdentity getObji() {
        return obji;
    }

    /**
     * <p>Original spec-file type: ObjectIdentity</p>
     * 
     * 
     */
    @JsonProperty("obji")
    public void setObji(ObjectIdentity obji) {
        this.obji = obji;
    }

    public DeleteNarrativeParams withObji(ObjectIdentity obji) {
        this.obji = obji;
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
        return ((((("DeleteNarrativeParams"+" [obji=")+ obji)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
