
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
 * <p>Original spec-file type: ListAvailableTypesParams</p>
 * <pre>
 * workspaces - list of items where each one is workspace name of textual ID.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspaces"
})
public class ListAvailableTypesParams {

    @JsonProperty("workspaces")
    private List<String> workspaces;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("workspaces")
    public List<String> getWorkspaces() {
        return workspaces;
    }

    @JsonProperty("workspaces")
    public void setWorkspaces(List<String> workspaces) {
        this.workspaces = workspaces;
    }

    public ListAvailableTypesParams withWorkspaces(List<String> workspaces) {
        this.workspaces = workspaces;
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
        return ((((("ListAvailableTypesParams"+" [workspaces=")+ workspaces)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
