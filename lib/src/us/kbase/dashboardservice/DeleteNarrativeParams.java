
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
    "wsi"
})
public class DeleteNarrativeParams {

    /**
     * <p>Original spec-file type: WorkspaceIdentity</p>
     * 
     * 
     */
    @JsonProperty("wsi")
    private WorkspaceIdentity wsi;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

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

    public DeleteNarrativeParams withWsi(WorkspaceIdentity wsi) {
        this.wsi = wsi;
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
        return ((((("DeleteNarrativeParams"+" [wsi=")+ wsi)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
