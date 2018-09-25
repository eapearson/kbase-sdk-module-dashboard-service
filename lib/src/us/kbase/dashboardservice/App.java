
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
 * <p>Original spec-file type: App</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "id",
    "notFound",
    "title",
    "subtitle",
    "iconURL"
})
public class App {

    @JsonProperty("id")
    private String id;
    @JsonProperty("notFound")
    private Long notFound;
    @JsonProperty("title")
    private String title;
    @JsonProperty("subtitle")
    private String subtitle;
    @JsonProperty("iconURL")
    private String iconURL;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("id")
    public String getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(String id) {
        this.id = id;
    }

    public App withId(String id) {
        this.id = id;
        return this;
    }

    @JsonProperty("notFound")
    public Long getNotFound() {
        return notFound;
    }

    @JsonProperty("notFound")
    public void setNotFound(Long notFound) {
        this.notFound = notFound;
    }

    public App withNotFound(Long notFound) {
        this.notFound = notFound;
        return this;
    }

    @JsonProperty("title")
    public String getTitle() {
        return title;
    }

    @JsonProperty("title")
    public void setTitle(String title) {
        this.title = title;
    }

    public App withTitle(String title) {
        this.title = title;
        return this;
    }

    @JsonProperty("subtitle")
    public String getSubtitle() {
        return subtitle;
    }

    @JsonProperty("subtitle")
    public void setSubtitle(String subtitle) {
        this.subtitle = subtitle;
    }

    public App withSubtitle(String subtitle) {
        this.subtitle = subtitle;
        return this;
    }

    @JsonProperty("iconURL")
    public String getIconURL() {
        return iconURL;
    }

    @JsonProperty("iconURL")
    public void setIconURL(String iconURL) {
        this.iconURL = iconURL;
    }

    public App withIconURL(String iconURL) {
        this.iconURL = iconURL;
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
        return ((((((((((((("App"+" [id=")+ id)+", notFound=")+ notFound)+", title=")+ title)+", subtitle=")+ subtitle)+", iconURL=")+ iconURL)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
