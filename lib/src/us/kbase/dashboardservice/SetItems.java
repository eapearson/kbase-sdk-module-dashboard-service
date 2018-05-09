
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
import us.kbase.common.service.Tuple11;


/**
 * <p>Original spec-file type: SetItems</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "set_items_info"
})
public class SetItems {

    @JsonProperty("set_items_info")
    private List<Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>>> setItemsInfo;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("set_items_info")
    public List<Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>>> getSetItemsInfo() {
        return setItemsInfo;
    }

    @JsonProperty("set_items_info")
    public void setSetItemsInfo(List<Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>>> setItemsInfo) {
        this.setItemsInfo = setItemsInfo;
    }

    public SetItems withSetItemsInfo(List<Tuple11 <Long, String, String, String, Long, String, Long, String, String, Long, Map<String, String>>> setItemsInfo) {
        this.setItemsInfo = setItemsInfo;
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
        return ((((("SetItems"+" [setItemsInfo=")+ setItemsInfo)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
